'''
do techno-economic-analysis calculation
changed version ->
'''
import math
import numpy as np

from dataclasses import dataclass
#from aux.materialbalance import MaterialBalance
#TODO: add O2-revenues
#TODO: consider units
#TODO: clc costs for clc_externalCompression
#TODO: combine all years (e.g. wrt lifetime, etc)

# TODO: insert economy of scale! (PROOST capex !!!)
# TODO: CORRECT: tIns ->
@dataclass
class AuxVal():
    pass



def econ(self, bsc_par, tec_par, elec_par, surch_par, cpx_par, matbal,
                teares, yr): # CstPar_in, eC, mat_in, signm):
    ''' adopted from CS_Mod/Eco_clc_oop_v063.py '''


    ### adjust matbal (make separate function!!)
    # adj = False
    matbal['t_simu'] = matbal.get('t_simu', 8760)
    matbal['E_util_act'] =  matbal.get('E_util_act', matbal.get('E_util',None))
    matbal['E_util_DC'] =  matbal.get('E_util_DC', False)
    print('matbal (in econ): ', matbal)


    #Mat = self.mat
    #Tec = self.par['teco_'+self.tec_el] #tec specific parameters | dict
    #''' CAUTION: glbPar -> not tec-specific'''
    #Mat = self.matbal_data

    # TODO collect all necessary values FIRST (and check them), then calc.

    # TODO: Include Storage costs
    # -> cost for cavern/vessel
    # -> cost bop (capex/opex)
    # -> cost compression (electricity)
    if matbal['m_H2']<=0:
        skip=True
    else:
        skip=False

    if not skip:
        clc_auxVal(self, bsc_par, tec_par, cpx_par, matbal,teares, yr)

        self.av = AuxVal()
        ''' >>>>>>>>>>>>>>>>> check and edit below !! <<<<<<<<<<<<<<<<<<<<<< '''

        ### fixed costs
        teares['costs_capitalinvest'] = clc_capitalCosts(self, bsc_par, tec_par,
                                                                matbal,teares) # €/a

        teares['costs_maintenance'] = clc_maintenanceCosts(self, bsc_par, tec_par,
                                                                matbal,teares) # €/a

        ### variable costs
        (teares['costs_stackreplacement'],
            k_strpl_spc) = clc_strplCosts(self, teares['capital_costs_stack'],
                                                teares['el_pwr_nom'],
                                                matbal['t_op_el'],
                                                bsc_par, tec_par, matbal,
                                                teares)

        clc_electricityCosts(self, matbal,#matbal['E_util_act'], matbal['E_util_DC'],
                                bsc_par, tec_par, elec_par, surch_par,
                                matbal, teares, yr)

        (teares['costs_taxesandinsurances'],
        teares['costs_labor'],
        teares['costs_water'] ) = clc_additionalCosts(self, teares['capex_tot'],
                                                            bsc_par, tec_par,
                                                                matbal,teares)

        teares['revenues_oxygen'] = clc_oxygenrevenues(self, bsc_par, tec_par,
                                                            matbal,teares)

        k_cap_cvrn, k_op_cvrn = clc_storageCosts(self, bsc_par, tec_par, matbal,teares)

        if False: ### DELETE ???
            self.av.k_var_excl = sum([k_strpl, k_elc_excl, k_tIns, k_labor, k_water, k_oxy])
            self.av.k_var_incl = sum([k_strpl, k_elc_incl, k_tIns, k_labor, k_water, k_oxy])
            self.av.k_cap = k_cap
            self.av.k_mnt = k_mnt


        ### external compression
        # TODO: include external compression ---> no calc yet !!
        teares['costs_external_compression'] = clc_externalCompression(self,
                                                bsc_par, tec_par, matbal, teares)




        ###########################################
        #self.sum_Costs(Mat, Tec)
        # k_sum_inter = (k_cap + k_mnt + k_strpl + k_tIns + k_labor + k_water
        #                + k_oxy + k_cap_cmpr + k_elc_cmpr)
        clc_costsum_abs(self, bsc_par, teares)
        if False: ### ??? DELETE ???
            klst = [k_cap,k_mnt,k_strpl,k_tIns,k_labor,k_water,k_oxy,k_cap_cmpr,k_elc_cmpr]
            knms = ['k_cap','k_mnt','k_strpl','k_tIns','k_labor','k_water','k_oxy','k_cap_cmpr','k_elc_cmpr']
            for nm,ki in zip(knms,klst):
                print(f'{nm}: ', ki)

        if False:
            k_sum_excl =  k_sum_inter + k_elc_excl
            k_sum_incl = k_sum_inter + k_elc_incl
            k_sum_excl_DC =  k_sum_inter + k_elc_excl_DC
            k_sum_incl_DC = k_sum_inter + k_elc_incl_DC

        k_res = clc_spcfcCosts(self,
                                matbal.get('V_H2', 0), matbal.get('m_H2', 0),
                                matbal.get('t_simu', 0),
                                bsc_par, tec_par, matbal, teares)
        eta_res = clc_efficiency(self, bsc_par, tec_par, matbal, teares)




    ###########################################


    '''
    if self.glbPar.print_eco__k_values:
        print('frac. CAPEX+MNTN+EL(ex)/ k_sum :', (self.k_cap + self.k_mnt + self.k_el_excl) / self.k_sum_e)
        print('frac. CAPEX+MNTN+EL(in)/ k_sum :', (self.k_cap + self.k_mnt + self.k_el_incl) / self.k_sum_i)
        print('---------frac. k_EL(ex)/ k_sum :', (self.k_el_excl) / self.k_sum_e)
        print('---------frac. k_EL(in)/ k_sum :', (self.k_el_incl) / self.k_sum_i)
        print('---------frac. k_strpl/ k_sum :', (self.k_strpl)/self.k_sum_e)
    '''
    k_fix_keys = 'k_cap k_mnt'.split()
    k_var_keys = 'k_strpl k_tIns k_labor k_water k_elc_excl k_elc_incl'.split()
    k_res_keys = 'k_vol_H2_e k_vol_H2_i k_mss_H2_e k_mss_H2_i'.split()

    ### make nemdtuple
    #eco_resNT = namedtuple('eco_resNT', 'k_cap k_mnt k_el_e k_el_i k_strpl k_tins k_lab k_H2O k_sum_e k_sum_i k_H2_e k_H2_e_kg k_H2_i k_H2_i_kg eta_sys')
    #self.eco_Res = eco_resNT(self.k_cap, self.k_mnt, self.k_el_excl, self.k_el_incl, self.k_strpl, self.k_tins, self.k_lab, self.k_H2O, self.k_sum_e, self.k_sum_i, self.k_H2_e, self.k_H2_e_kg, self.k_H2_i, self.k_H2_i_kg, self.eta_sys)
    return

    '''
    def wrap_cpxclc(self):
        return
    '''


def clc_costsum_abs(self, bscpar, res):
    '''
    Calculate absolute operation costs

    '''
    c_keys = [item.replace('include_costs_', '') for item in bscpar.keys() if ('include_costs' in item) and ('electricity' not in item)]
    # knms = ['electricity','k_mnt','k_strpl','k_tIns','k_labor','k_water','k_oxy','k_cap_cmpr','k_elc_cmpr']
    # k_sum_inter = (k_cap + k_mnt + k_strpl + k_tIns + k_labor + k_water
    #                + k_oxy + k_cap_cmpr + k_elc_cmpr)

    costs = 0
    for key in c_keys:
        costs += bscpar.get('include_costs_'+key, False) * res.get('costs_'+key, False)
    revenues = res['revenues_oxygen']


    res['costsum_noelectricity'] = costs
    res['final_balance_noelectricity'] = costs + revenues


    f_keys = [item for item in res.keys() if '_electricity' in item]
    for key in f_keys:
        #if 'electricity' in key:
        newkey = key.replace('costs_electricity','')
        print('Clc costsum for : ', key)
        res['final_balance_'+newkey] = (res['final_balance_noelectricity'] +
                                        res[key])

    return costs, revenues


def clc_auxVal(self, bscpar, tecpar, cpxpar, mat, res, yr):

    #self.P_plnt = Mat.P_N / 1e3 # // in kW (P_N in W)
    #print('P_plnt: ', P_plnt, '-----','eCe, eCI: ', self.eCe,', ',self.eCi )
    print('(auxVAl) ', self.el_pwr_nom)#['el_pwr_nom'])
    ### annuity factor
    #i_r = Tec.iR     # // in 1
    i_r = tecpar['interest_rate']['value']/100
    tau = tecpar['lifetime_electrolyser']['value']  # // in a
    Af = ( i_r * (i_r + 1)**tau ) / ( ( ( i_r + 1 )**tau ) - 1 )
    #print('Af:', Af) # ~0.08 (tau=20a, iR=5%)

    if self.ext_scen:
        aC = mat['capex'] # capex value from external-matbal file in €/kW
    elif bscpar['fitting_fnctn_capital_costs']: # use fitting function for capex calc
        aC = capex_fit(self, self.el_pwr_nom, tecpar)
    elif bscpar['yearspecific_capital_costs']:
        aC = cpxpar['yrspc_plantaquisition'][str(yr)]
    else:
        # use fixed parameter value as capex
        aC = tecpar['costs_plantacquisition']['value'] # Acquisition costs of plant

    frc_StAcq = tecpar['fraction_stackacquisition_pacq']['value'] # Fraction of Stack acquisit.costs wrt plant
    StC_bare = aC * frc_StAcq         # Bare Stack costs (for sum of stacks in plants)
    res['capital_costs_stack'] = StC_bare

    EQP_C_woSt = aC * (1 - frc_StAcq) # EQP costs without Stack

    rF = tecpar['lang_factor']['value']
    #self.CAPEX_EL
    capex_el   = aC * (1 - frc_StAcq) * rF # CAPEX of electrolyzer || rF == lang_factor
    #self.CAPEX_St
    capex_st  = aC * frc_StAcq * rF         # CAPEX of Stack
    #self.CAPEX_tot
    capex_tot = aC * rF                      # Total CAPEX || rF == lang_factor

    res['annuity_factor'] = Af
    res['capex_el'] = capex_el
    res['capex_st'] = capex_st
    res['capex_tot'] = capex_tot

    return capex_tot


def capex_fit(self, P_in, tecpar):
    '''
    use capex-function, fitted from Proost 2019

    '''
    # TODO: external script for different capex-functions
    def ffun(p_in, a, b, c):
        '''
        fitted function based on Proost 2019
        p_in in MW
        '''
        return a * np.exp(b/p_in) + (c*p_in)

    cfpar = tecpar['capex_curve_fit']
    p_llmt = cfpar['lower_limit_plant_power']['value']
    k_llmt = cfpar['lower_limit_costs_plantacquisition']['value']
    #llmt = [2.1, 0.7] # Lower limit of plant power // in MW
    #k_lmt = [400, 545] # Lower limit of specific investment cost in €/MW
    #linf = [[[0.4,2000],[2,500]], [[0.2,3000],[0.6,2000]]] # Linear fit for AEL linf[0] and PEM linf[1] in low power range
    pow_lo = cfpar['fitting_coeff_lin']['lower_limit_power']
    pow_hi = cfpar['fitting_coeff_lin']['upper_limit_power']
    cost_lo = cfpar['fitting_coeff_lin']['lower_limit_costs']
    cost_hi = cfpar['fitting_coeff_lin']['upper_limit_costs']

    P_in = float(self.el_pwr_nom) # // in kW

    if P_in < p_llmt:
        # linear fit for low power values
        k_spec = P_in * ( (cost_hi - cost_lo) / (pow_hi - pow_lo) ) + cost_lo
        # TODO: check: what about add_klim for AEL ???
    else:
        # curve fit
        coeffs = cfpar['fitting_coeff_crv']
        p_in = P_in *1e-3 # Convert P_in to MW
        k_spec = ffun(p_in,*coeffs)

    # Extracted values from Proost2019 (Figure 4)
    # Might be checked...
    #aa,bb,cc = np.array([   [582.609751, 0.367851704, -1.03609829], # AEL
    #                         [737.069812, 0.375146694, -13.7710513] # PEM
    #                     ])[tec]
    # Linear regression in low power range
    #if P_in < llmt[tec]:
    #    k_spec = P_in*((linf[tec][0][1]-linf[tec][1][1]) / (linf[tec][0][0]-linf[tec][1][0]))+linf[tec][0][1]
    #    #print('P_in:',P_in,'k_spec',k_spec)
    #    add_klmt_ael = 689 # additional lower cost limit for AEL, based on Fig 3 (bend between single and multistack (?))
    #    if (tec == 0) & (k_spec < add_klmt_ael):
    #        k_spec = add_klmt_ael
    #else:
    #    k_spec = efun(P_in,aa,bb,cc) # Calc specific cost based on fitted function
    if k_spec < k_llmt: # Apply lower cost limit
        k_spec = k_llmt
    print('k_spec: ', k_spec)
    return k_spec

def clc_capitalCosts(self, bscpar, tecpar, mat, res):
    ### CAPEX
    #self.k_cap = self.glbPar.c_k_cap * P_plnt * Tec.aC * Tec.rF *self.Af # // in kW * €/kW * 1 * 1/a
    P_N = float(self.el_pwr_nom) # // in kW
    res['el_pwr_nom'] = P_N
    ccomp = bscpar['include_costs_capitalinvest'] # Choose/disable component |
    chcklst = [ccomp, P_N, res['capex_tot'], res['annuity_factor']]
    clstk = ['ccomp', 'P_N', 'res[capex_tot]', 'res[annuity_factor]']

    for key, elm in zip(clstk, chcklst):
        print(f'Key: {key} /// val: {elm} /// type: {type(elm)}')

    return ccomp * P_N * res['capex_tot'] * res['annuity_factor'] # capex_costs // in €/a



def clc_maintenanceCosts(self, bscpar, tecpar, mat, res):
    ### maintenance costs
    P_N = res['el_pwr_nom'] #float(self.el_pwr_nom) # // in kW
    mC = tecpar['costs_maintenance']['value'] #Maintenance costs, specific
    ccomp = bscpar['include_costs_maintenance'] # Choose/disable component |

    mC_tot = ccomp * P_N * mC # maintenance costs // kW * €/(kW a) # orig.: including 'tau'
    res['maintenance_costs'] = mC_tot
    return mC_tot


def clc_electricityCosts(self, matbal, #W_el_tot, W_el_DC,
                            bscpar, tecpar, elecpar, surchpar, mat, res,yr):

    ccomp = bscpar['include_costs_electricity'] # Choose/disable component |

    ### electricity costs
    # W_el_tot = mat['E_util_act']
    # W_el_DC = mat['E_util_DC']
    if not matbal.get('E_util_act') or not matbal.get('E_util_DC'):
        self.logger.warning('Apply Simple Calc E_DC = E_tot')
        W_el_tot = W_el_AC = matbal['E_util']
        W_el_DC = 0
    else:
        W_el_AC = W_el_tot - W_el_DC
    gen_key = self.tec_gen
    #elec_key = get_gentec_key(self, elecpar, gen_key)
    #self.tec_gen = elec_key


    ### grid operation


    ### RE operation (green H2)
    if False:
        if eSc == False:
            self.logger.info('No value for surcharges found in params')

        ### include option for W_el_AC < 1GWh ???

        if eSc_1gwh_AC_in == False:
            self.logger.info('No value for 1GWh-surcharges found in params')
        else:
            W_el_AC = W_el_AC - 1e6

        if eSc_1gwh_DC_in == False:
            self.logger.info('No value for 1GWh-surcharges found in params')
        else:
            W_el_DC = W_el_DC - 1e6



    if mat.get('CE_util',False) and self.CE_agora:
        print(' --- Calc elec costs from agora (CE) data --- ')
        k_elec_excl = mat['CE_util']
        print('CAUTION: surcharges disabled (using CE_util, ext)')
        k_elec_incl = 0 #k_elec_excl +(ccomp * W_el * (eSc+ eSc_1gwh))
        res['costs_electricity_excl'] = k_elec_excl # write to subdict of matbal
    else:

        if bscpar['yearspecific_electricity_costs']:
            xtrm = bscpar.get("extreme_electricity_costs","LO").upper()
            print(f' --- use year-specific par data ({xtrm}) for elec costs --- ')
            fctr = elecpar['yrspc_'+self.gen_key_elec+'_'+xtrm].get('factor',1)
            eCe = fctr * elecpar['yrspc_'+self.gen_key_elec+'_'+xtrm][str(yr)]
        else:
            print(' --- use par data for elec costs --- ')
            # elec_key = get_gentec_key(self, elecpar, gen_key)
            # self.tec_gen = elec_key
            fctr = elecpar[self.gen_key_elec].get('factor',1)
            eCe = fctr * elecpar[self.gen_key_elec]['value'] # Electricity costs without surcharges
        res['eCe'] = eCe
        k_elec_excl_AC = ccomp * W_el_AC * eCe # Excluding cost allocation   // in kWh/a * €/kWh
        k_elec_excl_DC = ccomp * W_el_DC * eCe # Excluding cost allocation   // in kWh/a * €/kWh
        k_elec_excl = k_elec_excl_AC + k_elec_excl_DC
        res['costs_electricity_excl'] = k_elec_excl # write to subdict of matbal


        modes = ['grid', 'DiRE']

        for mode in modes:
            clc_surcharges(surchpar, res, yr, mode, W_el_AC, W_el_DC)
            res['costs_electricity_incl_'+mode+'_AC'] = k_elec_excl + res['surcharges_'+mode+'_AC'] # write to subdict of matbal
            res['costs_electricity_incl_'+mode+'_DC'] = k_elec_excl + res['surcharges_'+mode+'_DC']
            res['costs_electricity_incl_'+mode+'_tot'] = k_elec_excl + res['surcharges_'+mode+'_DC']+ res['surcharges_'+mode+'_AC']


    return



def clc_surcharges(surchpar, res, yr, mode, W_el_AC, W_el_DC):
    '''
    Read/Calc surcharges in €/kWh

    '''
    key_AC = 'surcharges_'+mode+'_AC'
    key_DC = 'surcharges_'+mode+'_DC'

    eSc_AC = surchpar.get(key_AC,{}).get(yr,False) # Surcharges
    eSc_DC = surchpar.get(key_DC,{}).get(yr,False) # Surcharges for electrolyzer (Stack) only
    res['eSc_AC'] = eSc_AC
    res['eSc_DC'] = eSc_DC
    if mode == 'grid':
        eSc_1gwh_AC_in = surchpar['surcharges_1GWh_AC'].get(yr,False) # Surcharges for first GWh AC
        eSc_1gwh_DC_in = surchpar['surcharges_1GWh_DC'].get(yr,False) # Surcharges for first GWh DC

        W_el_AC = W_el_AC -1e6
        W_el_DC = W_el_DC -1e6
        eSc_1gwh_AC = (eSc_1gwh_AC_in * 1e6) / (W_el_AC) #mat['E_util']
        eSc_1gwh_DC = (eSc_1gwh_DC_in * 1e6) / (W_el_DC)

    elif mode == 'DiRE':
        eSc_1gwh_AC = 0
        eSc_1gwh_DC = 0

    print(' -------- | Mode: ', mode)
    k_AC = res[key_AC] = (eSc_AC + eSc_1gwh_AC) * W_el_AC
    k_DC = res[key_DC] = (eSc_DC + eSc_1gwh_DC) * W_el_DC

    print(' -------- | Surcharges AC: ',(eSc_AC + eSc_1gwh_AC))
    print(' -------- | Surcharges DC: ', (eSc_DC + eSc_1gwh_DC))

    return (k_AC, k_DC)


def clc_strplCosts(self, StC_bare, # capital costs Stack
                            P_N,  # Nominal Power of plant
                            t_op_el,
                        bscpar, tecpar, mat, res, **kwargs):
    ### stack replacement
    #self.k_strpl = self.glbPar.c_k_strpl * ( Tec.aC * Tec.iCst_frc / Tec.lt_st ) * Mat.t_op * P_plnt
    lt_St = tecpar['lifetime_stack']['value'] # // in h
    lt_el = tecpar['lifetime_electrolyser']['value'] # // in a
    ''' edit 202111 in order to calc stackreplacemant for full period of simu'''
    if bscpar.get('strpl_var',False):
        n_strpl = bscpar.get('set_n_strpl',0)
    elif self.t_op_st_tot is not None:
        t_op_st_tot = self.t_op_st_tot
        n_strpl = math.ceil(((t_op_st_tot / self.n_yrs) * lt_el) / lt_St) -1 # Number of events of stackreplacement
    else:
        ''' new method taking into account replacement every n years and 1 existing stack (in CAPEX)'''
        # print('mat in clc_StrplC: ', mat)
        effective_lifespan_St = (lt_St / t_op_el ) #mat['t_op_el'])
        if np.isnan(effective_lifespan_St):
            effective_lifespan_St = 0
            n_strpl = 0
        else:
            n_strpl = math.ceil(lt_el / effective_lifespan_St) -1# number of additional stack(s) to be replaced (every n operation hours)

    # ===========
    print('mat[t_op_el]:', mat['t_op_el'])
    # print('effective_lifespan_St: ', effective_lifespan_St)
    print('n_yrs: ', self.n_yrs)
    print('lt_St: ', lt_St)
    print('lt_el: ', lt_el)
    print('t_op_st_tot: ', self.t_op_st_tot)
    print('n_strpl: ', n_strpl)

    ccomp = bscpar['include_costs_stackreplacement']

    # StC_bare = res['capital_costs_stack']
    # P_N = res['el_pwr_nom'] #float(self.el_pwr_nom)

    k_strpl_spc = n_strpl *  StC_bare / lt_el # // in €/Stack * Stacks / operation_time
    # P_N = res['el_pwr_nom']
    k_strpl = ccomp * k_strpl_spc * P_N
    if 'test' in kwargs:
        print('tec: ', self.tec)
        print('Tec.lt_st || Mat.t_op || Tec.lt_el', Tec.lt_st,'||', Mat.t_op,'||', Tec.lt_el)
        print('bare_Stack_Costs: ', self.StC_bare)
        print('effective lifespan: ', self.effective_lifespan_St)
        print('test in kwargs: ', kwargs.get('test'))
        print('self.n_strpl: ', self.n_strpl)
        print('k_strpl_spc: ', self.k_strpl_spc)
        print('k_strpl: ', self.k_strpl)

    res['stackreplacement_costs'] = k_strpl
    res['stackreplacement_costs_specific'] = k_strpl_spc
    return k_strpl, k_strpl_spc


def clc_additionalCosts(self, k_cap_tot, bscpar, tecpar, mat, res):
    ### taxes and insurances

    # k_cap_tot = res['capex_tot']

    ccomp_tIns = bscpar['include_costs_taxesandinsurances']
    tIns = tecpar['costs_taxesandinsurances']['value']
    k_tIns = ccomp_tIns * tIns * k_cap_tot
    # DONE: tIns should not be applied to total (not annual) capex !
    if np.isnan(k_tIns):
        k_tIns = 0

    ### labor costs
    ccomp_lab = bscpar['include_costs_labor']
    lC = tecpar['costs_labor']['value']
    num_supv = tecpar['number_supervisor_per_plant']['value'] # (fraction)
    t_supv = tecpar['time_plant_supervision']['value'] #
    t_lab_spc = t_supv * num_supv # labor hours for electrolyser
    k_lab = ccomp_lab * lC * t_lab_spc
    if np.isnan(k_lab):
        k_lab = 0

    ### water costs
    ccomp_wat = bscpar['include_costs_water']
    wC = tecpar['costs_diwater']['value'] # Costs of water
    k_H2O = ccomp_wat * wC * mat['m_H2O'] * 1e-3 # // in €/t * kg/a * 0.001 t/kg = €/a
    if np.isnan(k_H2O):
        k_H2O = 0

    res['taxesandinsurances_costs'] = k_tIns
    res['labor_costs'] = k_lab
    res['water_costs'] = k_H2O

    return k_tIns, k_lab, k_H2O


def clc_oxygenrevenues(self, bscpar, tecpar, mat, res):
    '''
    returns revenues for oxygen (negative cost-value)
    '''
    ccomp = bscpar['include_revenues_oxygen']
    oxy_rev = tecpar['revenue_oxygen']['value'] # // in €/ kg
    k_oxy = ccomp * -abs(oxy_rev) * mat['m_O2']
    if np.isnan(k_oxy):
        k_oxy = 0
    res['revenues_oxygen'] = k_oxy
    return k_oxy


def clc_storageCosts(self, bscpar, tecpar, mat, res):
    ccomp = bscpar['include_costs_storage']
    '''
    consider specific cost-factor ?
    '''
    if ccomp:
        strg_teco_par = self.par['teco_storage']
        # TODO: strg_0 (Storage name) hardcoded !!!

        strg_par = self.scen_par['parameters']['parameters_strg']['strg_0']
        if self.scen_par is not None:
            if strg_par and (not self.scen_par['parameters']['parameters_strg']['multiple']):

                ccap_cvrn = (strg_par['capacity_volume']['value']
                                * strg_teco_par['investmentcosts_volumetric']['value'])
                if ccap_cvrn is None:
                    ccap_cvrn = (strg_par['capacity_mass']['value']
                                * strg_teco_par['investmentcosts_gravimetric']['value'])
                copx_cvrn = 0 #* strg_teco_par['costs_maintenance_spc']['value']
    else:
        self.logger.info(' --- Skip clc_StrgCosts --- ')
        ccap_cvrn = 0
        copx_cvrn = 0
    # copx_cvrn = mat['E_cmp'] * price

    return ccomp*ccap_cvrn, ccomp*copx_cvrn


def clc_externalCompression(self, bscpar, tecpar, mat, res):
    ccomp = bscpar['include_costs_external_compression']
    k_cap_cmpr = 0
    if mat.get('CE_cmp',False):
        k_elc_cmpr = mat['CE_cmp']
    else:
        k_elc_cmpr = 0
    print(' (teconas l.351) clc_costs of Compression not implemented !!!')
    # P_cmp # in kW
    res['k_cap_ext_cmpr'] = k_cap_cmpr
    res['k_elec_ext_cmpr'] = k_elc_cmpr
    return 0


def sum_Costs(self, Mat, Tec):
    ### resulting hydrogen costs
    self.k_sum_woel = (self.k_cap + self.k_mnt + self.k_strpl + self.k_tins + self.k_lab + self.k_H2O)
    self.k_sum_e = self.k_sum_woel + self.k_el_excl
    self.k_sum_i = self.k_sum_woel + self.k_el_incl
    return

def clc_spcfcCosts(self, V_H2, m_H2, t_simu,
                        bscpar, tecpar, mat, res):
    # k_sum_e, k_sum_i = k_sums
    # k_sum_e_DC, k_sum_i_DC = k_sums_DC


    #mb = Materialbalance() # default: STP
    #V_H2 = mat['m_H2'] / mb.Hydrogen.rho # // in Nm³
    #V_O2 = mat['m_O2'] / mb.Oxygen.rho # // in Nm³
    #print('mat: ', mat)
    skey = 'final_balance'
    if V_H2 >0: #mat.get('V_H2'):
        if False:
            k_vol_H2_e = k_sum_e / V_H2 #mat['V_H2']
            k_vol_H2_i = k_sum_i / V_H2 #mat['V_H2']
            # DC (Stack)
            k_vol_H2_e_DC = k_sum_e_DC / V_H2 #mat['V_H2']
            k_vol_H2_i_DC = k_sum_i_DC / V_H2 #mat['V_H2']

    keys = [item for item in res.keys() if skey in item]
    for key in keys:
        if skey in key:
            newkey = key.replace(skey,'')
            if V_H2 >0: #mat.get('V_H2'):
                res['volumetric_costs_H2_'+newkey] = res[key] / V_H2 #mat['V_H2']

            # m_H2 = mat['m_H2']
            res['gravimetric_costs_H2_'+newkey] = res[key] / m_H2 #mat['m_H2']



    else:
        self.logger.info('No data for volumetric clc -> skip ')
        k_vol_H2_e = 0
        k_vol_H2_i = 0

    #res['volumetric_costs_H2_excl'] = k_vol_H2_e
    #res['volumetric_costs_H2_incl'] = k_vol_H2_i
    #res['volumetric_costs_H2_excl_DC'] = k_vol_H2_e_DC
    #res['volumetric_costs_H2_incl_DC'] = k_vol_H2_i_DC

    #k_mss_H2_e = k_sum_e / mat['m_H2']
    #k_mss_H2_i = k_sum_i / mat['m_H2']
    #k_mss_H2_e_DC = k_sum_e_DC / mat['m_H2']
    #k_mss_H2_i_DC = k_sum_i_DC / mat['m_H2']

    #res['gravimetric_costs_H2_excl'] = k_mss_H2_e
    #res['gravimetric_costs_H2_incl'] = k_mss_H2_i
    #res['gravimetric_costs_H2_excl_DC'] = k_mss_H2_e_DC
    #res['gravimetric_costs_H2_incl_DC'] = k_mss_H2_i_DC

    ############################################################################
    # V_H2 = mat.get('V_H2', 0)
    # m_H2 = mat.get('m_H2', 0)

    t_simu = mat.get('t_simu')
    k_fix = res['costs_capitalinvest'] + res['costs_maintenance']
    k_var = sum([res['costs_stackreplacement'],
                 res['costs_taxesandinsurances'],
                 res['costs_labor'], res['costs_water'],
                 res['revenues_oxygen'],
                 res['costs_electricity_excl']])

    (res['gravimetric_costs_H2_projected'],
        res['volumetric_costs_H2_projected']) =clc_costprojection(k_var,
                                                                    k_fix,
                                                                    m_H2,
                                                                    V_H2,
                                                                    t_simu)


    ### clc also for separate parts
    keylst = ['capitalinvest', 'maintenance', 'stackreplacement',
    'taxesandinsurances', 'labor', 'water', 'revenues_oxygen', 'electricity_excl']

    for k in keylst:
        if not 'revenues' in k:
            key = 'costs_'+k
        else:
            key = k
        res[key+'_spc'] = res.get(key)/m_H2

    if False:
        ### projected costs
        # time spec. amounts
        if t_simu >0: #mat.get('t_simu'):
            k_e_tspc = self.av.k_var_excl / t_simu #mat['t_simu']
            k_i_tspc = self.av.k_var_incl / t_simu #mat['t_simu']


            skip_proj = False
        else:
            self.logger.info('No data for projected clc -> skip ')
            k_e_tspc = 0
            k_i_tspc = 0
            t_proj = 8760 # projected operational time of electrolysis
            t_fctr = 0 #8760/mat['t_simu']
            skip_proj = True


        k_fix = self.av.k_cap + self.av.k_mnt


        if mat.get('V_H2'):
            k_vol_H2_e_proj = (k_fix + k_e_tspc*t_proj) / (V_H2*t_fctr) #(mat['V_H2']*t_fctr)
            k_vol_H2_i_proj = (k_fix + k_i_tspc*t_proj) / (V_H2*t_fctr) #(mat['V_H2']*t_fctr)
        else:
            self.logger.info('No data for volumetric clc (proj) -> skip ')
            k_vol_H2_e_proj = 0
            k_vol_H2_i_proj = 0
        res['volumetric_costs_H2_excl_projected'] = k_vol_H2_e_proj
        res['volumetric_costs_H2_incl_projected'] = k_vol_H2_i_proj

        if not skip_proj:
            k_mss_H2_e_proj = (k_fix + k_e_tspc*t_proj) / (m_H2*t_fctr) #(mat['m_H2']*t_fctr)
            k_mss_H2_i_proj = (k_fix + k_i_tspc*t_proj) / (m_H2*t_fctr) #(mat['m_H2']*t_fctr)
        else:
            k_mss_H2_e_proj =0
            k_mss_H2_i_proj =0
        res['gravimetric_costs_H2_excl_projected'] = k_mss_H2_e_proj
        res['gravimetric_costs_H2_incl_projected'] = k_mss_H2_i_proj

    return #(k_vol_H2_e, k_vol_H2_i), (k_mss_H2_e, k_mss_H2_i)

def clc_efficiency(self, bscpar, tecpar, mat, res):
    if not mat.get('E_LHV_H2', False):
        mat['E_LHV_H2'] = mat['m_H2'] * 33.3
    if not mat.get('E_HHV_H2', False):
        mat['E_HHV_H2'] = mat['m_H2'] * 39.4

    res['eta_sys_LHV']  = mat['E_LHV_H2'] / mat['E_util_act']
    res['eta_sys_HHV']  = mat['E_HHV_H2'] / mat['E_util_act']
    res['eta_st_LHV']   = (mat['E_LHV_H2'] / mat['E_util_DC']) if mat['E_util_DC'] >0 else 0
    res['eta_st_HHV']   = (mat['E_HHV_H2'] / mat['E_util_DC']) if mat['E_util_DC'] >0 else 0

    return


def clc_costprojection(k_var, k_fix, m_H2, V_H2, t_simu):
    '''
    Cost projection for incomplete simulation (< 1yr)
    '''
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    t_proj = 8760 # CHECK !!!! !!!! ????
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    t_fctr = t_proj/t_simu #mat['t_simu']

    k_tspc = k_var / t_simu #mat['t_simu']

    if V_H2 >0:
        k_proj_vol = (k_fix + k_tspc*t_proj) / (V_H2*t_fctr)
    else:
        k_proj_vol = 0

    k_proj_grav = (k_fix + k_tspc * t_proj) / (m_H2*t_fctr)


    return k_proj_grav, k_proj_vol




def clc_emissions(self, bscpar, tecpar, mat, res):

    return

################################################################################
def check_pwr(self):
    ''' additional output in simu-df needed (?)
    '''
    return

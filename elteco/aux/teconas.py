'''
do techno-economic-analysis calculation
'''
import math
import numpy as np
#from aux.materialbalance import MaterialBalance
#TODO: add O2-revenues
#TODO: consider units
#TODO: clc costs for clc_externalCompression
#TODO: combine all years (e.g. wrt lifetime, etc)

def run_teconas(self, ):
    bsc_par = self.par['basic']
    par_tec = self.par['teco_'+self.tec_el] #tec specific parameters | dict
    matbal = self.matbal_data #matbal data | dict
    par_elec = self.par['electricity_costs']



    for yr, mb_yr in matbal.items():
        tea_res = {}
        econ(self, bsc_par, par_tec, par_elec, mb_yr, tea_res)

        mb_yr['tea_'+str(yr)] = tea_res
    # TODO: combine econas for all years

    print('         --------  Finished teconas     ----------       ')
    #print('final dict: ', self.matbal_data)
    return

def econ(self, bsc_par, tec_par, elec_par, matbal, teares):#CstPar_in, eC, mat_in, signm):
    ''' adopted from CS_Mod/Eco_clc_oop_v063.py '''
    #Mat = self.mat
    #Tec = self.par['teco_'+self.tec_el] #tec specific parameters | dict
    #''' CAUTION: glbPar -> not tec-specific'''
    #Mat = self.matbal_data


    clc_auxVal(self, bsc_par, tec_par, matbal,teares)

    ''' >>>>>>>>>>>>>>>>> check and edit below !! <<<<<<<<<<<<<<<<<<<<<< '''

    ### fixed costs
    k_cap = clc_capitalCosts(self, bsc_par, tec_par, matbal,teares)

    k_mnt = clc_maintenanceCosts(self, bsc_par, tec_par, matbal,teares)

    ### variable costs
    k_strpl, k_strpl_spc = clc_strplCosts(self, bsc_par, tec_par, matbal,teares)

    k_elc_excl, k_elc_incl = clc_electricityCosts(self, bsc_par, tec_par, elec_par, matbal,teares)

    k_tIns, k_labor, k_water = clc_additionalCosts(self, bsc_par, tec_par, matbal,teares)

    k_oxy = clc_oxygenrevenues(self, bsc_par, tec_par, matbal,teares)

    ### external compression
    # TODO: include external compression ---> no calc yet !!
    k_cap_cmpr, k_cmpr = clc_externalCompression(self, bsc_par, tec_par, matbal, teares)




    ###########################################
    #self.sum_Costs(Mat, Tec)
    k_sum_inter = (k_cap + k_mnt + k_strpl + k_tIns + k_labor + k_water
                    + k_oxy + k_cap_cmpr + k_cmpr)
    k_sum_excl =  k_sum_inter + k_elc_excl
    k_sum_incl = k_sum_inter + k_elc_incl

    k_res = clc_spcfcCosts(self, bsc_par, tec_par, matbal, teares, (k_sum_excl, k_sum_incl))
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

def clc_auxVal(self, bscpar, tecpar, mat, res):

    #self.P_plnt = Mat.P_N / 1e3 # // in kW (P_N in W)
    #print('P_plnt: ', P_plnt, '-----','eCe, eCI: ', self.eCe,', ',self.eCi )

    ### annuity factor
    #i_r = Tec.iR     # // in 1
    i_r = tecpar['interest_rate']['value']
    tau = tecpar['lifetime_electrolyser']['value']  # // in a
    Af = ( i_r * (i_r + 1)**tau ) / ( ( ( i_r + 1 )**tau ) - 1 )
    #print('Af:', Af) # ~0.08 (tau=20a, iR=5%)
    aC = tecpar['costs_plantacquisition']['value'] # Acquisition costs of plant
    frc_StAcq = tecpar['fraction_stackacquisition_pacq']['value'] # Fraction of Stack acquisit.costs wrt plant
    StC_bare = aC * frc_StAcq         # Bare Stack costs
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


def clc_capitalCosts(self, bscpar, tecpar, mat, res):
    ### CAPEX
    #self.k_cap = self.glbPar.c_k_cap * P_plnt * Tec.aC * Tec.rF *self.Af # // in kW * €/kW * 1 * 1/a
    P_N = float(self.el_pwr_nom) # // in kW
    res['el_pwr_nom'] = P_N
    ccomp = bscpar['include_costs_capitalinvest'] # Choose/disable component |
    chcklst = [ccomp, P_N, res['capex_tot'], res['annuity_factor']]
    clstk = ['ccomp', 'P_N', 'res[capex_tot]', 'res[annuity_factor]']
    #for key, elm in zip(clstk, chcklst):
    #    print(f'Key: {key} /// val: {elm} /// type: {type(elm)}')

    return ccomp * P_N * res['capex_tot'] * res['annuity_factor'] # capex_costs // in €/a



def clc_maintenanceCosts(self, bscpar, tecpar, mat, res):
    ### maintenance costs
    P_N = res['el_pwr_nom'] #float(self.el_pwr_nom) # // in kW
    mC = tecpar['costs_maintenance']['value'] #Maintenance costs, specific
    ccomp = bscpar['include_costs_maintenance'] # Choose/disable component |

    mC_tot = ccomp * P_N * mC # maintenance costs // kW * €/(kW a) # orig.: including 'tau'
    res['maintenance_costs'] = mC_tot
    return mC_tot


def clc_electricityCosts(self, bscpar, tecpar, elecpar, mat, res):
    ### electricity costs
    W_el = mat['E_util']
    gen_key = self.tec_gen
    elec_key = get_gentec_key(self, elecpar, gen_key)
    eCe = elecpar[elec_key]['value'] # Electricity costs without surcharges
    eSc = elecpar['surcharges_electricity_default']['value'] # Surcharges
    ccomp = bscpar['include_costs_electricity'] # Choose/disable component |
    k_elec_excl = ccomp * W_el * eCe # Excluding cost allocation   // in kWh/a * €/kWh
    res['electricity_costs_excl'] = k_elec_excl # write to subdict of matbal
    k_elec_incl = ccomp * W_el * (eCe + eSc) # Including cost alloc.       // in kWh/a * €/kWh
    res['electricity_costs_incl'] = k_elec_excl # write to subdict of matbal
    return k_elec_excl, k_elec_incl


def clc_strplCosts(self, bscpar, tecpar, mat, res, **kwargs):
    ### stack replacement
    #self.k_strpl = self.glbPar.c_k_strpl * ( Tec.aC * Tec.iCst_frc / Tec.lt_st ) * Mat.t_op * P_plnt
    ''' new method taking into account replacement every n years and 1 existing stack (in CAPEX)'''
    lt_St = tecpar['lifetime_stack']['value'] # // in h
    lt_el = tecpar['lifetime_electrolyser']['value'] # // in a
    effective_lifespan_St = (lt_St / mat['t_op_el'])
    if np.isnan(effective_lifespan_St):
        effective_lifespan_St = 0
        n_strpl = 0
    else:
        n_strpl = math.ceil(lt_el / effective_lifespan_St) -1# number of additional stack(s) to be replaced (every n operation hours)

    ccomp = bscpar['include_costs_stackreplacement']
    StC_bare = res['capital_costs_stack']
    P_N = res['el_pwr_nom'] #float(self.el_pwr_nom)
    k_strpl_spc = n_strpl *  StC_bare / lt_el # // in €/Stack * Stacks / operation_time
    P_N = res['el_pwr_nom']
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


def clc_additionalCosts(self, bscpar, tecpar, mat, res):
    ### taxes and insurances
    k_cap = res['capex_tot']
    ccomp_tIns = bscpar['include_costs_texasandinsurances']
    tIns = tecpar['costs_taxesandinsurances']['value']
    k_tIns = ccomp_tIns * tIns * k_cap
    res['taxesandinsurances_costs'] = k_tIns

    ### labor costs
    ccomp_lab = bscpar['include_costs_labor']
    lC = tecpar['costs_labor']['value']
    num_supv = tecpar['number_supervisor_per_plant']['value'] # (fraction)
    t_supv = tecpar['time_plant_supervision']['value'] #
    t_lab_spc = t_supv * num_supv # labor hours for electrolyser
    k_lab = ccomp_lab * lC * t_lab_spc
    res['labor_costs'] = k_lab

    ### water costs
    ccomp_wat = bscpar['include_costs_water']
    wC = tecpar['costs_diwater']['value'] # Costs of water
    k_H2O = ccomp_wat * wC * mat['m_H2O'] * 1e-3 # // in €/t * kg/a * 0.001 t/kg = €/a
    res['water_costs'] = k_H2O

    return k_tIns, k_lab, k_H2O


def clc_oxygenrevenues(self, bscpar, tecpar, mat, res):
    '''
    returns revenues for oxygen (negative cost-value)
    '''
    ccomp = bscpar['include_revenues_oxygen']
    oxy_rev = tecpar['revenue_oxygen']['value'] # // in €/ kg
    k_oxy = ccomp * -abs(oxy_rev) * mat['m_O2']
    res['oxygen_revenues'] = k_oxy
    return k_oxy

def clc_externalCompression(self, bscpar, tecpar, mat, res):
    return 0, 0


def sum_Costs(self, Mat, Tec):
    ### resulting hydrogen costs
    self.k_sum_woel = (self.k_cap + self.k_mnt + self.k_strpl + self.k_tins + self.k_lab + self.k_H2O)
    self.k_sum_e = self.k_sum_woel + self.k_el_excl
    self.k_sum_i = self.k_sum_woel + self.k_el_incl
    return

def clc_spcfcCosts(self, bscpar, tecpar, mat, res, k_sums):
    k_sum_e, k_sum_i = k_sums

    #mb = Materialbalance() # default: STP
    #V_H2 = mat['m_H2'] / mb.Hydrogen.rho # // in Nm³
    #V_O2 = mat['m_O2'] / mb.Oxygen.rho # // in Nm³
    #print('mat: ', mat)
    k_vol_H2_e = k_sum_e / mat['V_H2']
    res['volumetric_costs_H2_excl'] = k_vol_H2_e
    k_vol_H2_i = k_sum_i / mat['V_H2']
    res['volumetric_costs_H2_incl'] = k_vol_H2_i

    k_mss_H2_e = k_sum_e / mat['m_H2']
    k_mss_H2_i = k_sum_i / mat['m_H2']

    return (k_vol_H2_e, k_vol_H2_i), (k_mss_H2_e, k_mss_H2_i)

def clc_efficiency(self, bscpar, tecpar, mat, res):
    eta_sys         = mat['E_LHV_H2'] / mat['E_util']
    res['eta_sys'] = eta_sys
    return eta_sys

################################################################################
def check_pwr(self):
    ''' additional output in simu-df needed (?)
    '''
    return

def get_gentec_key(self, dct, gen_key):
    peeg = self.par['basic']['post_eeg']
    ret_key = None
    while not ret_key:
        for key in dct.keys():
            if gen_key in key:
                splt = key.split(gen_key)[-1]
                if peeg and splt:
                    ret_key = key
                elif not peeg and not splt:
                    ret_key = key
        if not ret_key:
            gen_key = input(f'Simu: {self.name}: \n No entry found in electricity parameters for key: {gen_key}'
                    + f'\n please insert valid key {dct.keys()}')

    '''
    splt = key.split(gen_key)
        if splt[-1]:
            lst.append(gen_key+splt[-1])
    '''

    return ret_key

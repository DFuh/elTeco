'''
do techno-economic-analysis calculation
'''

#TODO: add O2-revenues

def econ(self):#CstPar_in, eC, mat_in, signm):
        ''' adopted from CS_Mod/Eco_clc_oop_v063.py '''
        #Mat = self.mat
        Tec = self.par['teco_'+self.tec_el]
        ''' CAUTION: glbPar -> not tec-specific'''

        clc_auxVal(self, Mat, Tec)

        ''' >>>>>>>>>>>>>>>>> check and edit below !! <<<<<<<<<<<<<<<<<<<<<< '''

        clc_capitalCosts(Mat, Tec)

        self.clc_maintenanceCosts(Mat, Tec)

        self.clc_strplCosts(Mat, Tec)

        self.clc_electricityCosts(Mat, Tec)

        self.clc_additionalCosts(Mat, Tec)

        ###########################################
        self.sum_Costs(Mat, Tec)

        self.clc_spcfcCosts(Mat, Tec)
        self.clc_efficiency(Mat, Tec)

        ###########################################


        '''
        if self.glbPar.print_eco__k_values:
            print('frac. CAPEX+MNTN+EL(ex)/ k_sum :', (self.k_cap + self.k_mnt + self.k_el_excl) / self.k_sum_e)
            print('frac. CAPEX+MNTN+EL(in)/ k_sum :', (self.k_cap + self.k_mnt + self.k_el_incl) / self.k_sum_i)
            print('---------frac. k_EL(ex)/ k_sum :', (self.k_el_excl) / self.k_sum_e)
            print('---------frac. k_EL(in)/ k_sum :', (self.k_el_incl) / self.k_sum_i)
            print('---------frac. k_strpl/ k_sum :', (self.k_strpl)/self.k_sum_e)
        '''

        ### make nemdtuple
        eco_resNT = namedtuple('eco_resNT', 'k_cap k_mnt k_el_e k_el_i k_strpl k_tins k_lab k_H2O k_sum_e k_sum_i k_H2_e k_H2_e_kg k_H2_i k_H2_i_kg eta_sys')
        self.eco_Res = eco_resNT(self.k_cap, self.k_mnt, self.k_el_excl, self.k_el_incl, self.k_strpl, self.k_tins, self.k_lab, self.k_H2O, self.k_sum_e, self.k_sum_i, self.k_H2_e, self.k_H2_e_kg, self.k_H2_i, self.k_H2_i_kg, self.eta_sys)
        return


    def wrap_cpxclc(self):
        pass


    def clc_auxVal(self, Mat, Tec):
        self.P_plnt = Mat.P_N / 1e3 # // in kW (P_N in W)
        #print('P_plnt: ', P_plnt, '-----','eCe, eCI: ', self.eCe,', ',self.eCi )

        ### annuity factor
        #i_r = Tec.iR     # // in 1
        i_r = self.par.
        tau = Tec.lt_el  # // in a
        self.Af = ( i_r * (i_r + 1)**tau ) / ( ( ( i_r + 1 )**tau ) - 1 )
        #print('Af:', Af) # ~0.08 (tau=20a, iR=5%)

        self.StC_bare = Tec.aC * (Tec.iCst_frc)         # Bare Stack costs
        self.EQP_C_woSt = Tec.aC * (1 - Tec.iCst_frc) # EQP costs without Stack

        self.CAPEX_EL   = Tec.aC * (1 - Tec.iCst_frc) * Tec.rF # CAPEX of electrolyzer || rF == lang_factor
        self.CAPEX_St   = Tec.aC * Tec.iCst_frc * Tec.rF         # CAPEX of Stack
        self.CAPEX_tot  = Tec.aC * Tec.rF                      # Total CAPEX || rF == lang_factor
        return


    def clc_capitalCosts(self, Mat, Tec):
        ### CAPEX
        #self.k_cap = self.glbPar.c_k_cap * P_plnt * Tec.aC * Tec.rF *self.Af # // in kW * €/kW * 1 * 1/a
        self.k_cap = self.glbPar.c_k_cap * self.P_plnt * self.CAPEX_tot * self.Af # // in €/a
        #print('k_cap:', self.k_cap)
        return


    def clc_maintenanceCosts(self, Mat, Tec):
        ### maintenance costs
        self.k_mnt = self.glbPar.c_k_mnt * self.P_plnt * Tec.mC # // kW * €/(kW a) # orig.: including 'tau'
        return


    def clc_electricityCosts(self, Mat, Tec):
        ### electricity costs
        self.k_el_excl = self.glbPar.c_k_el * Mat.W_el * self.eCe # Excluding cost allocation   // in kWh/a * €/kWh
        self.k_el_incl = self.glbPar.c_k_el * Mat.W_el * self.eCi # Including cost alloc.       // in kWh/a * €/kWh
        return


    def clc_strplCosts(self, Mat, Tec, **kwargs):
        ### stack replacement
        #self.k_strpl = self.glbPar.c_k_strpl * ( Tec.aC * Tec.iCst_frc / Tec.lt_st ) * Mat.t_op * P_plnt
        ''' new method taking into account replacement every n years and 1 existing stack (in CAPEX)'''
        self.effective_lifespan_St = (Tec.lt_st / Mat.t_op)
        self.n_strpl = math.ceil(Tec.lt_el / self.effective_lifespan_St) -1# number of additional stack(s) to be replaced (every n operation hours)

        self.k_strpl_spc = self.n_strpl *  self.StC_bare / Tec.lt_el # // in €/Stack * Stacks / operation_time
        self.k_strpl = self.k_strpl_spc * self.P_plnt
        if 'test' in kwargs:
            print('tec: ', self.tec)
            print('Tec.lt_st || Mat.t_op || Tec.lt_el', Tec.lt_st,'||', Mat.t_op,'||', Tec.lt_el)
            print('bare_Stack_Costs: ', self.StC_bare)
            print('effective lifespan: ', self.effective_lifespan_St)
            print('test in kwargs: ', kwargs.get('test'))
            print('self.n_strpl: ', self.n_strpl)
            print('k_strpl_spc: ', self.k_strpl_spc)
            print('k_strpl: ', self.k_strpl)
        return


    def clc_additionalCosts(self, Mat, Tec):
        ### taxes and insurances
        self.k_tins = self.glbPar.c_k_tIns * Tec.tIns * self.k_cap

        ### labor costs
        self.k_lab = self.glbPar.c_k_lab * Tec.lC * self.glbPar.t_lab_spc

        ### water costs
        self.k_H2O = self.glbPar.c_k_wat * Tec.wC * Mat.m_H2O * 1e-3 # // in €/t * kg/a * 0.001 t/kg = €/a
        return


    def sum_Costs(self, Mat, Tec):
        ### resulting hydrogen costs
        self.k_sum_woel = (self.k_cap + self.k_mnt + self.k_strpl + self.k_tins + self.k_lab + self.k_H2O)
        self.k_sum_e = self.k_sum_woel + self.k_el_excl
        self.k_sum_i = self.k_sum_woel + self.k_el_incl
        return

    def clc_spcfcCosts(self, Mat, Tec):
        V_H2 = Mat.m_H2 / self.glbPar.rho_H2 # // in Nm³

        self.k_H2_e = self.k_sum_e / V_H2
        self.k_H2_i = self.k_sum_i / V_H2

        self.k_H2_e_kg = self.k_sum_e / Mat.m_H2
        self.k_H2_i_kg = self.k_sum_i / Mat.m_H2
        return

    def clc_efficiency(self, Mat, Tec):
        self.eta_sys         = (Mat.m_H2 * self.glbPar.LHV_H2_m) / Mat.W_el
        return

    def check_pwr(self):
        ''' additional output in simu-df needed (?)
        '''
        return

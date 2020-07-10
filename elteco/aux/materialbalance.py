'''
make material balance
'''

### check script in spyder: test_class_materialbalance

class MaterialBalance():
    ### basic parameters
    # Standard State: p = 10^5 Pa, arbitrarily, but fixed T
    # STP:  p = 10^5 Pa,    T = 273.15 K
    # NTP:  p = 101325 Pa,  T = 293.15 K (NIST)
    # ISMC: p = 101325 Pa,  T = 288.15 K

    M_H2        = 2.01588 * 10**(-3)    # molar mass of hydrogen // in kg/mol
    spec_E_H2   = 33.3                  # specific energy content of hydrogen // kWh/kg

    M_O2        = 31.9988 * 10**(-3) # molar mass of oxygen // in kg/mol

    M_H2O       = 18.01528 * 10**(-3) # molar mass of water // in kg/mol

    #rho_H2      = 0.0899 # // in kg/m³ @ 273 K
    #rho_H2O_STP = 999.793 # // in kg/ m³
    #rho_H2O     = 998.2 #980 in kg/m³ #rho_H2O     = 0.9982 # density of water @T= 20°C in kg/dm³

    p0 = 101325 # // in Pa
    T0 = 273.15 #

    global F
    F = 96485 # // in C/mol
    global R
    R = 8.314 # // in J/ mol K

    LHV_H2_m    = 33.32                # lower heating valuein kWh/kg

    def __init__(self, T=None, p=None):
        if not T:
            self.T = self.T0
        if not p:
            self.p = self.p0
        self.Hydrogen = self.Gases(M=self.M_H2, T=self.T, p= self.p)
        self.Oxygen = self.Gases(M=self.M_O2, T=self.T, p= self.p)




    def process_df(self, ):
        '''
        input data must contain:
        date        | n_H2      | n_O2      | n_H2O     | P_in   | P_act
        pd.datetime | in mol/s  | in mol/s  | in mol/s  | in kW  |  in kW
        '''

        return


    def clc_materialbalance(self, df, stats=True, sig_stats=True):
        '''
        calculate amounts of educts/ products
        and operation stats
        '''

        #df = ?
        df['dt_s'] = (df.time-df.time.shift(1)).dt.seconds #total_seconds()
        df['dt_hr'] = df.dt_s / 3600
        m_H2 = sum(df.n_H2 * df.dt_s * self.M_H2) # amount of produced Hydrogen // in kg
        m_O2 = sum(df.n_O2 * df.dt_s * self.M_O2) # amount of produced Oxygen // in kg
        m_H2O = sum( abs(df.n_H2O) * df.dt_s * self.M_H2O) # amount of consumed Water // in kg

        E_util = df.P_act * df.dt_s # amount of utilized energy // in kWh
        E_in = df.P_in* df.dt_s # amount of available energy from EE // in kWh

        if stats:
            #TODO: distinguish between P_st and P_act !!!
            t_op_EL = np.where(df.P_act >0, 1,0) * df.dt_hr# operation time of electrolyser
            t_fl_EL = None # full load hours of electrolyser

        if sig_stats:
            t_op_EE = None # operation time of ee plant(s)
            t_fl_EE = None # full load hours of ee plant(s)

        return ?


    class Gases():

        def __init__(self,M=None,T=None, p=None ):
            super().__init__()
            self.rho = self.clc_density(M, T, p )
            pass

        def clc_density(self,M,T,p):
            rho = (M*p) / (super().R * T)
            return rho

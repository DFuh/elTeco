'''
simple calculation of electrolyzer power based on
- fraction (function*) of auxilliary power consumption
- electrolyzer efficiency (constant**)

-- do not mix it up !!!

'''

# TODO: *function for AEL missing /// both hve to be validated
# TODO: **implement function for eff. -> based on? E_H2/time ??

# TODO: implement method for fiiting/ regression of characteristic curve (efficiency, power consumpt., ...)

from handlefiles import handleInputFiles as hif # not working

class elPower():
    def __init__():
        self.Pmax = 0#?
        self.vmax = 0#?
        self.tec = 0#?
        # read EE-power df |CHECK|

        self.df = self.make_input_df()
        self.mat_df = None


    def make_input_df(self, ):
        '''
        processing input data for simple calc
        '''
        sig_df_raw = hif.read_file()
        sig_df_clean = hif.clean_df()
        # rename columns |CHECK|
        sig_df_0 = hif.rename_columns(sig_df_raw)

        return sig_df_0


    def make_simple_calc(df):
        '''

        '''
        df['P_theo'], df['P_aux'] = clc_Ptheo(df.P)
        return df


    def clc_Ptheo(pin, tec):
        '''
        calc theoretical utilisable power
        '''
        pfrac_aux = powPerc(pin, tec)
        ptheo = pin/(1+pfrac_aux)
        paux = ptheo*pfrac_aux
        ## fagiacomo:
        return ptheo, paux



    def powerPerc_switch():
        '''
        different functions for fraction of auxilliary power
        '''
        return

    def powPercPEM(P):
        x = P/PN*6
        powPerc = 79.153*(x**-0.975)
        return powPerc/100

# clc P theoretical
# clc P auxilliary

# make materialbalance

'''
Calcl electricity surcharges based on selected law
'''


class Surcharges():

    '''
    CLc-modes:
        - ppa       [Power Purchase Agreement -> green H2]
        - dire      [Direct Coupling with RE -> green H2]
        - grid      [ Grid operation, electricity intensive industry]
        - default   [no remission]
    '''

    def __init__(self, mode):
        self.mode =  mode


    def check_mode(self,):
        '''
        Check if mode is valid
        '''
        return

    def clc_levy(self, baseval):
        '''
        Calc resulting levy
        '''


        return

'''
handling of parameter reading and processing
'''
import glob
import os
import collections
import json

class handleParams():
    '''
    select version of parameter sets
    read and convert each to df
    '''
    #TODO: enable parameter input via xls
    #TODO: add descriptive text in json files ?

    def __init__(self, basepath, test=False):
        self.lst_parfiles = glob.glob(basepath+'/par/*.json')

        #print(self.lst_parfiles)
        self.print_filelist(self.lst_parfiles, name='Parameter')
        if not test:
            self.parameter_version = self.select_par_version()
        self.dct = self.read_params(basepath, test)

        print(" --- finished parameter reading --- ")

    def print_filelist(self, fllst, name=None):
        '''
        print elements of list
        --->>>move to aux-files
        '''
        print('The List ({}) contains the following files:'.format(name))
        for item in fllst:
            print(os.path.basename(item))#+'\n')
        return


    def select_par_version(self):
        
        vers_input = input('Insert parameter version to be used: [integer/key] (any key -> default)')

        try:
            version = int(vers_input)
            print('Parameter version: ', version)
        except:
            print('Using default parameters...')
            version = None
        return version


    def read_params(self,pth0, test):
        '''
        read parameter files based on version
        '''

        #df_par = []#[df_bscpar, df_ecpar, df_tecopar_ael, df_tecopar_pem]
        dct_par = {}
        par_strng = ['basic',
                    'electricity_costs',
                    'teco_AEL',
                    'teco_PEM',
                    'external_scenario']
        #for dfi, pthi in

        if test:
            suffix = '_test.json'
        elif not self.parameter_version:
            suffix = '_default.json'
        else:
            suffix = '_v' + self.parameter_version + '.json'

        for pthi in par_strng:
            jsonpth = pth0 + '/par/params_' + pthi + suffix

            #df_par.append(self.json_to_df(jsonpth))
            #print(jsonpth)
            with open(jsonpth) as jsonfile:
                data=json.load(jsonfile)
                #print(data)
                #df_par.append(data)
                dct_par[pthi] = data


        '''
        Parnatu = collections.namedtuple('Parnatu', 'basic ec teco_ael teco_pem ext_scen')
        Par_dfs = Parnatu._make([df_par[0],
                df_par[1],
                df_par[2],
                df_par[3],
                df_par[4]])
        '''

        return dct_par #Par_dfs
    '''
    def mk_params_pth(pth0, paths, vers=False):


        fin_paths = []
        for pthi, fpthi in zip(paths, finpaths):
            fpthi.append()
        return
    '''
    '''
    def json_to_df(self, jsonpth):
        print('Open file: {}'.format(jsonpth))
        # easier to use pandas directly
        ''''''
        with open(jsonpth) as json_data:
            data = json.load(json_data)

        print('data (json): ', data)
        df = pd.DataFrame(data).T
        ''''''
        data = pd.read_json(jsonpth, orient='index')
        return data
    '''

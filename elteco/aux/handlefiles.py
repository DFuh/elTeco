'''
function in EL_Teco
handle files for ...
'''
import glob
import os
import collections
import json
import pandas as pd
import tkinter
###
class handleInputFiles():
    """ main handling of files
    """
    def __init__(self, basepath, params):
        self.basic_par = params.dfs.basic
        self.input_pth = None

        # create path to ...???
        #self.mk_fl_pth()
        #self.datasource = self.selectsource()

        # choose data source (material balance) for calculation






#######################################
    def file_path():
        # 0 -> default: simu-results file in data/in
        # 1 -> data from par
        # 2 -> existing materialbalance
        # 3 -> external file-source (path from pars OR browse)
        # 4 -> ??? from sig-df ->> SIMPEL

        return

    def mk_fl_pth(self):
        ### create storga path for material balance
        self.sto_fl_pth = (self.glbPar.pth +'/'
        +self.glbPar.sto_dirnm+'/'
        +'Mat_'+self.glbPar.sto_flnm+'.csv')
        ### create storga path for TEA results
        return


    def browse_pth(self):
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window

        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            #print("You chose %s" % tempdir)
            pth_out = tempdir
        else:
            pth_out = None
        return pth_out

    def read_sourcedata(self, path_to_file, specs=None):
        sim_data = None
        return sim_data


    def selectsource(self):
        '''
        select source of data for running TEA on
        '''
        src = self.basic_par.lower()
        try:
            int_src = int(src)
        else:
            int_src = None

        # 4 -> from sig-df
        if (src == 4) OR ('simpel' in src:
            print(' -- running simpEL as source -- ')
            print(' source-directory: ', self.sto_fl_pth)
            self.mk_fllst()
            if not self.fllst:
                print(' +++ no files found +++')
            else:
                self.data_src_nm = 'fllst'

        elif (int_src == 3) OR ('ext' in src:
            print(' -- browse external file -- ')
            pth = self.browse_pth()

        elif (int_src == 2) OR ('int' in src:
            print(' -- checking for existing data -- ')
            self.check_mat_data()
            if not self.mat_exists:
                print(' +++ no existing material-balance-data +++ ')
                answ1 = input('read from filelist? (y/n)')
                if answ1 == 'y':
                    self.data_src_nm = 'fllst'
                    self.mk_fllst()
            else:
                self.data_src_nm = 'df'

        elif src == 2:
            print(' -- using manually inserted data -- ')
            self.data_src_nm = 'man_lst'

        elif (src == 0) OR ('default' in src:
            pass
        else:
            print(' --  using example source -- ')
            print(' source-directory: ', self.sto_fl_pth)
            self.mk_fllst()
            if not self.fllst:
                print(' +++ no files found +++')
            else:
                self.data_src_nm = 'fllst'
        return

    def data_from_json(self,):
        ''' make dataset (.csv) from parameter file
        '''
        df = pd.read_json(orient='index').T
        df = df.reset_index()

        return

class handleOutputFiles():

    def __init(self):
        self.output_path = None
        self.filename_materialbalance = None
        self.filename_teco_results = None

        pass

class handleParams():
    '''
    select version of parameter sets
    read and convert each to df
    '''
    #TODO: enable parameter input via xls
    #TODO: add descriptive text in json files ?

    def __init__(self, basepath):
        self.lst_parfiles = glob.glob(basepath+'/par/*.json')
        self.print_filelist(self.lst_parfiles, name='Parameter')
        self.parameter_version = self.select_par_version()
        self.dfs = self.read_params(basepath)
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


    def read_params(self,pth0):
        '''
        read parameter files based on version
        '''

        df_par = []#[df_bscpar, df_ecpar, df_tecopar_ael, df_tecopar_pem]
        par_strng = ['basic',
                    'electricity_costs',
                    'teco_AEL',
                    'teco_PEM',
                    'external_scenario']
        #for dfi, pthi in

        if not self.parameter_version:
            suffix = '_default.json'
        else:
            suffix = '_v' + self.parameter_version + '.json'

        for pthi in par_strng:
            jsonpth = pth0 + '/par/params_' + pthi + suffix
            df_par.append(self.json_to_df(jsonpth))

        Parnatu = collections.namedtuple('Parnatu', 'basic ec teco_ael teco_pem ext_scen')
        Par_dfs = Parnatu._make([df_par[0],
                df_par[1],
                df_par[2],
                df_par[3],
                df_par[4]])


        return Par_dfs
    '''
    def mk_params_pth(pth0, paths, vers=False):


        fin_paths = []
        for pthi, fpthi in zip(paths, finpaths):
            fpthi.append()
        return
    '''
    def json_to_df(self, jsonpth):
        print('Open file: {}'.format(jsonpth))
        # easier to use pandas directly
        '''
        with open(jsonpth) as json_data:
            data = json.load(json_data)

        print('data (json): ', data)
        df = pd.DataFrame(data).T
        '''
        data = pd.read_json(jsonpth, orient='index')
        return data

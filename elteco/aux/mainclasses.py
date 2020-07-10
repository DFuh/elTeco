'''
main classes
output plot ?
'''
import os

try:
    import aux
except:
    pass
try:
    import aux.handlefiles as hf
except:
    import elteco.aux.handlefiles as hf
#from aux import elpower
#import aux.materialbalance as mb
#import aux.teconas as tea

#TODO: decide which parameter data-type to use dict, or df)
#TODO: write selected parameter-version to  ??? for subsequent use

##TODO: slelectsource !!

## CAPEX-Lit.: Saba, Proost

### define main
print('M: ', __name__)
#print('cwd: ', os.getcwd())

class elEco():
    """main class elEco."""

    def __init__(self, *args,basepath=None):

        #super(elEco, self).__init__()
        #self.arg = arg
        if not basepath:
            self.basepath = os.getcwd()
            print('self.basepath: ', self.basepath)
        else:
            self.basepath = basepath
        #print('current working directory: ', self.basepath)
        #TODO: decide, wether df or dict ! # currently Params -> dict
        self.Parameters = hf.handleParams(self.basepath)
        self.inFls = hf.handleInputFiles(self.basepath,self.Parameters)

        self.simuinst = self.make_simu_instances()
        #TODO: --> #self.simuInst =  # instances of

        #self.get_mat_data = self.sw_src(self.data_src_nm)

        #TODO: consider multiple par-tecos

        #TODO: make ouput of data/ file status

    def make_simu_instances(self):
        instances = []
        for fl in self.inFls.list_of_dicts:
            instances.append( elSimu( self.basepath, self.Parameters, fl, ) )
        #for ?? in ???:
        #    instances.append(elSimu())
        return instances

    def run_tea(self):
        print('...run techno-economical-assessment...')
        #check_mat_data(self)

        ### prepare files

        ### provide material data

        ### techno-economical assessment

        ### data output

        ### data visualization

        self.mk_fl_pth()
        #TODO: check, if mat-df exists: override or new flnm?
        self.cc_data_source()

        #self.get_mat_data() -> elSimu
        #self.mk_mat_df()  -> elSimu


        self.clc_eco()

        self.mk_full_df()

        return

    def make_instances(self, inst_params):

        inst_lst = []
        for item in fllst:
            inst_lst.append( elSimu( ) )
        return

class elSimu(elEco):
    """docstring for elSimu."""
    ''' instances of simulation-results'''

    def __init__(self, basepath, par, fl, source=None):
        #super(elSimu, self).__init__()
        #self.arg = None
        self.basepath = basepath
        self.par = par
        self.name = fl['name']
        self.file_list = fl['files']
        self.pth_lst = fl['full_flpth']
        self.nominal_power = fl['PN']
        self.tec = fl['tec']
        self.sig = fl['sig']
        self.years = fl['yrs']
        self.full_dict = fl
        self.df = fl['dfs']
        self.source = None
        self.oxy_reven = None
        self.info_dict = None
        self.skip = False # if True, dont consider in analysis
        self.print_status()

        self.matbal_pth_lst = self.mk_matbal_pth()
        self.matbal_data_lst = self.ctrl_matbal()
        '''
        self.matbal = mb.clc_materialbalance( ?? )
        '''
    def print_status(self, ):
        print('status ... -?-')
        return

    def ctrl_matbal(self):
        '''
        main-method for materialbalance
        '''
        # TODO: add selection: annual calc. or full (average) ???
        forced_clc = self.par.cont.basic['new_clc_matbal'] # parameter, forced new clc of matbal
        mb_data_lst = []

        for num, flpth in enumerate(self.pth_lst):
            mb_pth = self.matbal_pth_lst[num]
            file_exists = os.path.exists(mb_pth)

            if forced_clc or (not file_exists):
                # new calculation forced
                print('Calc materialbalance for file: {}'.format(self.name[num]))
                data_df = pd.read_csv(flpth)
                mb_df_raw = self.clc_matbal(data_df)
                mb_df.to_csv(mb_pth)
            else:
                print('material-balance-data already exists')
                self.skip_matbal = True
                mb_df_raw = pd.read_csv(mb_pth)

            mb_df = mb.process_df(mb_df_raw) ### yet to be edited

            mb_data_lst.append(mb_df)
        return mb_data_lst


    def mk_matbal_pth(self, ):
        '''
        create matbal-directory according to input file-location
        '''
        mat_pth_lst = []
        for pth in self.pth_lst: # pth list: full pth+filename.suffix
            pure_pth, flnm = os.path.split(pth) #full pth
            last_dir = os.path.basename(pure_pth)
            mat_pth0 = '/mat'
            dir_append = ''
            while last_dir != 'in':
                dir_append = last_dir+'/'+dir_append
                pure_pth = os.path.split(pure_pth)[0]
                last_dir = os.path.basename(pure_pth)
            mat_pth = mat_pth0+'/'+dir_append

            #dirnm = self.basepath
            #<<<< need relative path to file >>>>>
            newpath = self.basepath+'/data'+mat_pth
            full_filepath = newpath + '/MatBal__' + flnm
            mat_pth_lst.append(full_filepath)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
        ###########################################

        return mat_pth_lst


    def clc_matbal(self, filepath):
        '''
        clc materialbalance for every year of simu
        and write one row for each year in final df

        -- use existing matbal
        or
        -- clc matbal from simu-df
        or
        -- clcl matbal from simpleCLC (elpower)

        '''

        #for yr_i, df_i in self.full_dict['dfs'].items():
        for yr_i in self.years:

            df_i = self.full_dict['dfs'][yr_i]
            file_i = self.full_dict['files'][yr_i]
            if not self.full_dict['existing_matbal'][yr_i] and use_existing_matbal == False:
                if not df_i:
                    if smplSigClc == True:
                        pass
                        #elpower.
                    else:
                        # TODO: empty row in df -->>???
                        pass
                else:
                    mb_out = mb.clc_materialbalance(df_i)
            pass

        return

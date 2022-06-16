'''
main classes
output plot ?
'''
import os
import pandas as pd
import time
import glob
import datetime
try:
    import auxf
except:
    pass
try:
    from auxf import handlefiles as hf
    from auxf import handleparameters as hp
    from auxf import teconas as tea
except:
    from . import handlefiles as hf
    from . import handleparameters as hp
    from . import teconas as tea
import epos.auxf.writingfiles as wr
'''
try:
    import aux.handlefiles as hf
except:
    import handlefiles as hf
'''
#from aux import elpower
try:
    from auxf.materialbalance import MaterialBalance
    import auxf.faux as fx
except:
    from .materialbalance import MaterialBalance
    from . import faux as fx
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

    def __init__(self, basepath=None, pth_data_loc=None, test=False):

        #super(elEco, self).__init__()
        #self.arg = arg
        self.logger, self.logger_nm = fx.ini_logging(self, name='elEco')
        self.logger.info('Ini logging: {}'.format(self.logger_nm))
        if not basepath: # in case, basepath is not specified, use cwd
            self.basepath = os.getcwd()
        else:
            self.basepath = basepath
        print('self.basepath: ', self.basepath)
        #print('current working directory: ', self.basepath)
        #TODO: decide, wether df or dict ! # currently Params -> dict
        self.parameters = hp.handleParams(self.basepath, test=test) # read parameters, return dict

        # print('Parameters: \n', self.parameters.dct['external_scenario'])
        if True:
            self.inFls = hf.handleInputFiles(self.basepath, self.parameters.dct,
                                            pth_data_loc=pth_data_loc)
            # print('Props: ', self.inFls.dct_props)
        if True:
            self.simuinst = self.make_simu_instances()
        #TODO: --> #self.simuInst =  # instances of

        #self.get_mat_data = self.sw_src(self.data_src_nm)

        #TODO: consider multiple par-tecos

        #TODO: make ouput of data/ file status

    def make_simu_instances(self):
        instances = []
        # for num,fl in enumerate(self.inFls.list_of_dicts):
        for num,(tag,dct) in enumerate(self.inFls.dct_props.items()):
            print(f'{[num]}-----> Simu-Inst.: ', tag)
            # print('-----> Number of inst.: ', num)
            # print('-----> dict: ', fl)
            instances.append( elSimu( self.basepath, tag,
                                        self.parameters.dct,
                                        dct, self.inFls) )
        #for ?? in ???:
        #    instances.append(elSimu())
        return instances

    def run_tea(self):
        for num,inst in enumerate(self.simuinst):
            l = ['AAA','BBB','CCC','DDD']
            inst.run_technoeconomical_assessment(key=l[num])
        return


    def make_instances(self, inst_params):

        inst_lst = []
        for item in fllst:
            inst_lst.append( elSimu( ) )
        return


class elSimu(elEco):
    """docstring for elSimu."""
    ''' instances of simulation-results'''

    def __init__(self, basepath, tag, params, fld, inFls, source=None):
        #super(elSimu, self).__init__()
        #self.arg = None
        #print('---> fl in elSimu(): ', fl)
        # TODO: raise error, if len(name, tec, sig ) >1 ?
        self.inFls = inFls
        self.basepath = basepath
        print('basepath: ', basepath)
        #self.par = Par.ntpar # Params as NamedTuple:
        self.par = params # Parameters as dict
                             # basic, electricity_costs, teco_AEL, teco_PEM, external_scenario
        self.name = fld['name']
        self.tag = tag #fl['tag'][0] if hasattr(fl['tag'],'__len__') else fl['tag']

        self.fllst = fld['res_lst'] # fl['file']
        print('self.fllst = ', self.fllst)
        self.files = fld['files']
        print('self.files = ', self.files)
        self.pth_out = fld['pth_out']

        # self.scen_par = hf.input_scen_file(self)
        self.scen_par = fld['prm0']
        # print('scenf: ',self.scen_file)
        #self.pth_lst = fl['full_flpth']
        #self.nominal_power = fl['PN']
        print('dct ("fld"): ', fld)
        self.tec_el = fld['tec_el']
        self.tec_gen = fld['tec_gen']
        #====================================
        self.el_pwr_nom = fld.get('rpow_el', False) # Nominal power of EL-plant
        # self.el_pwr_max = fl['el_pwr_ol'] # Max power of EL-plant
        #====================================
        #self.sig = fl['sig']
        self.years = fld['years']
        self.n_yrs = len(self.years)
        self.full_dict = fld
        # self.df = fl['dfs']
        self.source = None
        self.oxy_reven = None
        self.info_dict = None
        self.skip = False # if True, dont consider in analysis

        self.logger, self.logger_nm = fx.ini_logging(self, )
        self.logger.info('Ini logging...: {}'.format(self.logger_nm))
        self.print_status()

        self.t_op_st_tot = None
        # self.matbal_pth_lst = self.mk_matbal_pth() # RENAME??? relative path from ref to matbal-directory
        self.matbal_pth_lst = self.inFls.dir_data_input
        if ('P_cnst' in self.inFls.dir_data_input) and self.par['basic']['enable_agoradata']:
            self.CE_agora = True
        else:
            self.CE_agora = False
        #self.matbal_data_lst = self.ctrl_matbal()
        self.matbal_data = self.ctrl_matbal()
        self.clc_t_op_tot()
        print('Matbal data ready: \n', self.matbal_data)
        '''
        self.matbal = mb.clc_materialbalance( ?? )
        '''

    def print_status(self, ):
        print('status ... -?-')
        #print('elSimu: ', self.__name__)
        print('elSimu: ', self.name)
        print('elSimu, files: ', self.files)

        return

    def clc_t_op_tot(self,):
        t_op_tot = 0
        n_yrs = 0
        yr_lst =[]
        for yr,data in self.matbal_data.items():
            t_op_tot += data['t_op_el']
            n_yrs +=1
            yr_lst.append(yr)
        self.t_op_st_tot = t_op_tot
        if self.n_yrs != n_yrs:
            print(' !! Deviation in Simu-years.... ')
        else:
            self.n_yrs = n_yrs
        return

    def run_technoeconomical_assessment(self, key=None, writefile=True):
        print('...run techno-economical-assessment...')
        #check_mat_data(self)

        tea.run_teconas(self, )
        self.tdd            = datetime.datetime.now()
        # self.today_ymd      = self.tdd.strftime("%Y%m%d")
        self.today_ymdhs    = self.tdd.strftime("%Y%m%d%H%M")
        ### save final df
        fin_df = pd.DataFrame.from_dict(self.matbal_data)
        # out_pth = self.par['basic']['dirname_data_location'][0]
        if key:
            flnm = self.name+'_'+self.tag+'_tearesults_'+self.today_ymdhs+'.json'
        outpth = os.path.join(self.pth_out,flnm)
        # outpth = outpath.replace('/in','/out')

        # n = 0
        # addz='0'
        #while os.path.exists(outpath):
        #     if n>9:
        #         addz = ''
        #     nmstr = '_'+addz+str(n)
        #     outpath.replace(outpath[-7:],nmstr)
        # outpth = outpth.replace('.csv','.json')
        # fin_df.to_csv(outpth)
        # --> changed to .json output
        self.matbal_data.update({'tag':self.tag})
        self.matbal_data.update({'name':self.name})
        self.matbal_data.update({'parameters':self.par})
        if writefile:
            print(' .... write results to json: ', outpth)
            wr.write_to_json(outpth, self.matbal_data)

        ### provide material data

        ### techno-economical assessment

        ### data output

        ### data visualization
        '''
        self.mk_fl_pth()
        #TODO: check, if mat-df exists: override or new flnm?
        self.cc_data_source()


        #self.get_mat_data() -> elSimu
        #self.mk_mat_df()  -> elSimu

        self.clc_eco()

        self.mk_full_df()
        '''
        return

    def ctrl_matbal(self):
        '''
        main-method for materialbalance
        '''
        print('>>> CTRL MATBAL')
        # TODO: add selection: annual calc. or full (average) ???

        ### mk path and dir
        yr0 = self.years[0]
        mb_pth = self.matbal_pth_lst #[0] # TODO: -> [num] ?
        print('mb_pth: ', mb_pth)
        #print('file_list[num]: ', self.files[yr0])
        if False:
            if not self.foreign_dir:
                abs_pth_mb = hf.mk_abspath(basepath=self.basepath, tar=mb_pth, cat='mat' )
                hf.mk_dir(abs_pth_mb)
                abs_pth_data = os.path.join(self.basepath, self.files[yr0])
            else:
                abs_pth_mb = mb_pth
        #print('year: ', str(yr))

        # flnm = os.path.basename(self.files[yr0].replace(str(yr0),'').replace('results', 'matbal'))
        # #flnm = flnm.replace('results', 'matbal')
        # flpth_mb = os.path.join(abs_pth_mb, flnm)
        #print('mb_pth: ', mb_pth)

        # file_exists = os.path.exists(flpth_mb)
        lst_matbal_files = glob.glob(mb_pth+'/*'+self.tag+'*matbal*.csv')
        if lst_matbal_files:
            if len(lst_matbal_files)>1:
                for k,item in enumerate(lst_matbal_files):
                    print(f'[{k}] -> ', item)
                try:
                    num = int(input('Found multiple matbal files...select valid one: [int]'))
                    file_exists = True
                    flpth_mb = lst_matbal_files[num]
                except:
                    print('invalid input -> calc new matbal')
                    file_exists = False
            elif len(lst_matbal_files) == 1:
                file_exists = True
                flpth_mb = lst_matbal_files[0]


        forced_clc = self.par['basic']['new_clc_matbal'] # parameter, forced new clc of matbal

        if forced_clc or (not file_exists):
            mb_data_lst = []
            mb_out = None
            for num, yr in enumerate(self.years): #self.pth_lst):
                # new calculation forced
                mb = MaterialBalance(self)

                print('Calc materialbalance for file: {}'.format(self.name))
                #data_df = pd.read_csv(abs_pth_data)
                # data_df = self.df[yr]
                data_df = dff = self.inFls.read_data_df(self.files[yr])[1]
                #mb_df_raw = self.clc_matbal(data_df)
                df_in = mb.process_df(data_df)
                if isinstance(df_in, pd.DataFrame):
                    df_out = mb.clc_materialbalance(df_in, yr)
                    if isinstance(mb_out, pd.DataFrame):
                        mb_out = mb_out.append(df_out, ignore_index=True)
                    else:
                        mb_out = df_out.copy()
                #mb_df.to_csv(mb_pth)
            mb_out.to_csv(flpth_mb, index=False)
            mb_out = mb_out.set_index('year')
            dct_mb = mb_out.T.to_dict() # TODO: unefficient!!! dict->df->dict (see:materialbalance)
        else:
            print('material-balance-data already exists')
            self.skip_matbal = True
            mb_out = pd.read_csv(flpth_mb)
            mb_out = mb_out.set_index('year')
            dct_mb = mb_out.T.to_dict()
            #mb_df = mb.process_df(mb_df_raw) ### yet to be edited

            #mb_data_lst.append(mb_df)

        return dct_mb



    def mk_matbal_pth(self, ):
        '''
        create matbal-directory according to input file-location

        [*** general version in EpoS ***]

        edit 20200817:
        more effective and improved version, considering input directly from simu-output-directory (or any specified dir)
        '''

        mat_pth_lst = []
        # basepath_data_output = self.basepath + '/data/out'
        #print('self.par.basic: ', self.par.basic)
        #if not hasattr(self.par.basic, 'dirname_data_location'):
        if not ('dirname_data_location' in self.par['basic']):
            splt_by = 'elTeco/elteco/data/in' # string to split path by; default: 'elTeco/elteco/data/in'
            try:
                end = testpath.split(splt_by)[1] #???
            except:
                end = None
                self.foreign_dir = True
        else:
            try:
                for loc, ref in zip(self.par['basic']['dirname_data_location'], self.par['basic']['reference_dirname_dat_loc']):

                    end = loc.split(ref)[1]
                    mat_pth_lst.append(end)
            except:
                for loc in self.par['basic']['dirname_data_location']:

                    # end = loc.split(ref)[1]
                    mat_pth_lst=[loc]
                    self.foreign_dir = True
        '''
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
        '''
        return mat_pth_lst


    def clc_matbal(self, df_i, yr_i):
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
        #for i, yr_i in enumerate(self.years):

        #df_i = self.full_dict['dfs'][yr] # Redundant code in ini
        #file_i = self.full_dict['files'][yr] #
        mb_out = None

        return mb_out

    def smpl_clc():
        if not df_i:
            if smplSigClc == True:
                pass
                #elpower.
            else:
                # TODO: empty row in df -->>???
                pass
        return

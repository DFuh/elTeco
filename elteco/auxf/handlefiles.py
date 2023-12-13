'''
function in EL_Teco
handle files for ...
'''
import glob
import os
import collections
import json
import numpy as np
import pandas as pd
import tkinter
###

# TODO: get_line()
# TODO: group and sort fllst (by year and/or tag)
# enable running program without installing tkinter

'''
see:
/home/dafu_res/0_modeling/py_scripts_v101/mod_3/data_output/csv_dataoutput_structure_v01.py

.../py_scripts_v101/csv/write_csv_v01.py # opt2 !
'''
print('Module: ', __name__)
print('cwd: ', os.getcwd())

# data from dir -> multiple scenarios
## specify/ distinguish on uuid and year


class handleInputFiles():
    """ main handling of files
    """
    def __init__(self, params, pth_data_loc=None, basepath=None):

        self.basepath = basepath
        self.yr_cnt = 0
        self.basic_par = params['basic'] # basic parameter dict
        if not pth_data_loc:
            self.dir_data_input = self.basic_par['dirname_data_location']
        else:
            self.dir_data_input = pth_data_loc
        self.fllst = self.mk_fllst_walk([self.dir_data_input])

        # self.fllst = self.mk_fllst() # make list of files (fullpath) containing simudata or sigdata
        print('----> fllst: ', self.fllst)

        self.dct_props = extr_data_properties(self.fllst) # |l. 764
        # self.list_of_dicts =
        # self.def_dict = self.ini_dict()
        # self.list_of_dicts = self.files_to_dicts(self.fllst)
        print('############### ----- created list of dicts...')


        #print(self.list_of_dicts)
        #
        #self.merge_dicts()

        #TODO: convert .xls data to csv
        #TODO: read multiple file formats? -> search_files()
        #TODO: reuse list_of-Dicts ???

        ### check if simu data ???

        ### ->>> get files
        ### ->>> make simple calc

        #fllst = glob.glob('./data/in/*.csv') #Caution: relative or absolute path??
        #print('files in /data/in: ', fllst)




        # create path to ...???
        #self.mk_fl_pth()
        #self.datasource = self.selectsource()

        # choose data source (material balance) for calculation


    def ini_dict(self,):
        d = {
            'name': None, #???
            'tag': None, # uuid
            'yrs': [],
            'tec': None,    # electrolysis technology
            'sig': None,    # input signal
            'PN': None,     # nominal power of electrolysis plant
            'npf': None,    # fraction of nominal renewable power input
            'files': None,
            'full_fpths': None,
            'dfs':   None,
            'existing_matbal': None
            }
        return d

    def mk_fllst(self, single_dir=True):
        # single or multiple ?
        # select source
        # fllst_raw = self.search_files(dirnms = self.basic_par['directory_names'],
        #                                 key = self.basic_par['selection_keys'])
        fllst_raw = self.search_files(dirnms = self.basic_par['dirname_data_location'],
                                         key = self.basic_par['selection_keys'])

        fllst_raw.sort()
        if not self.basic_par['manual_file_selection']:
            return fllst_raw
        else: #(additional) manual selection
            ### -- select files ?
            for num, fl in enumerate(fllst_raw):
                print('fl: ',num,'->', fl)
            # return list of integers for indexing (for selection out of filelist)

            # TODO: input check -> non valid input: return None, close progr.
            idx = list(map(int, list(input('select items: [int, int,..]').split(','))))

            fllst = [fllst_raw[i] for i in idx]
            ####
        ###

        #check, if multiple years

        # read and sort files !!!
        #print('fllst: ', fllst)
        return fllst


    def files_to_dicts(self, fllst):
        '''
        aim: sort files in list by tag or filename

        --> make list of dicts:
        [{'name': ?,
        'tag': >uuid<,
        'yrs': [2017,2018],
        'tec': 'PEM',
        'sig': 'WEA',
        'files': {'2017': file1_2017.csv, '2018': file2_2018.csv}
        'dfs':   {'2017': df_2017, '2018': df_2018}
        'existing_matbal': {'2017': False, '2018': False}},
        ]

        '''
        # reading
        # check, if info-text exists
        # check, if matbal exists
        list_of_dicts = []

        for fl in fllst: # fllst contains full paths
            dct, dff = self.read_data_df(fl, ini=True)
            # dct, df_skpr = self.read_specs(fl)
            #print('df_skpr: ', df_skpr)
            #dct['df'] = pd.read_csv(fl,skiprows=(df_skpr), parse_dates=[0])
            # dff = pd.read_csv(fl,skiprows=(df_skpr), index_col=[0], nrows=10) # REad only slice of df (read in full df later in simuinst)
            dfu = dff[dff.index == 'units']
            df = dff[dff.index !='units']
            #print('df: ', df.head())
            # df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d HH:%MM:%SS')
            # print(df.head(4))
            # df['Date'] = pd.to_datetime(df['Date'],unit='ns')
            dct['df'] = df
            dct['file'] = fl
            list_of_dicts.append(dct)

        final_list = self.merge_lod(list_of_dicts)
        #sfllst = sorted(my_list, key=lambda k: k['name'])
        ### options:
        # filename: tec, sig,
        # tag
        return final_list

    def unique_list(self,sequence):
        '''
        return list with unique objects, preserve original order
        '''
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]

    def print_it(self, iterator):
        for num, item in enumerate(iterator):
            print('{} --> {}'.format(num, item))
        return


    def merge_lod(self, lod, group_by='tag'): #input: list of dicts
        '''
        merge list of dicts
        '''
        #print('list of dicts:', lod)
        #self.logger.info('Merge lod...')

        df = pd.DataFrame(lod)      # make df from lod
        #print('df_od: ', df)
        inter1 = df.groupby(group_by)  # group by tags
        #self.print_it(inter1)
        #>>>> still an error below: <<<<<<<
        #TODO: what, if no tag ?

        cols = next(iter(inter1))[1].columns.tolist() # get column names /// easier way ??

        d_list  =  []                           # initialize output list
        for thing in inter1:                    # loop trough pd.groupby object /// returns tuple for each group
            #print('thing: ',thing)
            grp = inter1.get_group(thing[0])    # get group by sort-name
            #lst = []
            d = {}                              # initialize output dict
            for cnm in cols:                    # loop trough group

                if not 'df' in cnm:
                    d[cnm] = self.unique_list(grp[cnm].tolist())  # put items in list, remove duplicates
                    #print(unique(grp[cnm].tolist()))
                else:
                    d[cnm] = grp[cnm].tolist()          # removing duplicates doesnt work for dataframes

            #dct = dict(zip(d['yrs'],d['files']))        # put files in subdict (for calling by year)
            #df_dct = dict(zip(d['yrs'],d['dfs']))       # put dfs in subdict (for calling by year)
            dct = dict(zip(d['year'],d['file']))        # put files in subdict (for calling by year)
            df_dct = dict(zip(d['year'],d['df']))       # put dfs in subdict (for calling by year)
            d['files'] = dct
            d['dfs'] = df_dct
            d_list.append(d)
        #print('-->' ,dct)
        return d_list
    '''
    def merge_dicts(lst_of_dicts):
        ''''''
        see: https://stackoverflow.com/questions/36271413/pandas-merge-nearly-duplicate-rows-based-on-column-value#36271553

        see: https://stackoverflow.com/questions/2067627/python-list-of-dicts-how-to-merge-keyvalue-where-values-are-same

        merge spec dicts based on tags
        input: list of specs-dicts
        ''''''
        # split list based on key: 'tag'
        tag_lst = []
        notag_lst = []
        for dct in lst_of_dicts:
            if 'tag' in dct:
                tag_lst.append(dct)
            else:
                notag_lst.append(dct)

        ### only, if tag in infos
        if tag_lst:
            df = pd.DataFrame(tag_lst)
            df = df.set_index('yrs') #yrs
            grpd = df.groupby(['tag']) #tag
        else:


        lod_out = []
        for item in grpd:
            lod_out.append(item[1].T.to_dict('index'))

        if notag_lst:
            #TODO: ...
            # merge dicts with specs in filenames
            pass
        return lod_out
    '''

    def mk_fllst_walk(self,pth):


        # fl_dct = {}
        fllst = []
        for pthi in pth:
            print('pthi (fllst_walk): ', pthi)
            for root, dirs, files in os.walk(pthi):
                for dirn in dirs:
                    npth = os.path.join(root, dirn)
                    print('npth: ', npth)
                    parfiles = mk_filelist(npth, sffx='.json')
                    fllst += parfiles
                for file in files:
                    fpth = os.path.join(root, file)
                    print('fpth: ', fpth)
                    #parfiles = mk_filelist(fpth, sffx='.json')
                    flnm = os.path.basename(file)
                    if ('parameters' in flnm) & ('.json' in flnm):
                        fllst.append(fpth) #parfiles
                    # dct = extr_data_properties(parfiles) # |l. 764
                    # fl_dct.update(dct)
        fllst_o = self.unique_list(fllst)
        return fllst_o




    def search_files(self, dirnms=None, key=None):
        '''
        check different locations for files to use
        dirnm -> lst of paths
        key -> lst of keys to select files on (one for all or one each)
        '''
        #TODO: Option: browse path

        spth_lst = []
        fllst = []
        #if not matbal: # search with key

        for nm in dirnms: # select, wether to use default or spec path
            if 'nopath' in nm.lower(): # use default path
                spth = './data/in' # TODO: check for duplication with file_pth()
            else: # use specified path
            #<<<<<<<<<<< still problem with path
                spth = dirnms[0]
                #spth = self.basepath+dirnm[0] # TODO: enable multiple paths
            spth_lst.append(spth)
        print('search directories: ', spth_lst)
        for num,spth in enumerate(spth_lst):
            #print('glob-output: ', glob.glob(spth + '/*'+self.basic_par['file_format'][0]))
            for fl in glob.glob(spth + '/*'+self.basic_par['file_format'][0]): # TODO: enable multi formats???
                #print('fl:', fl)
                if not key:
                    fllst.append(fl)
                elif len(key)>1:
                    for k in key:
                        if k in fl:
                            fllst.append(fl)
                    else:
                        if key in fl:
                            fllst.append(fl)
                else:
                    if key in fl:
                        fllst.append(fl)

        return fllst # return list of files in dir (fullpath)


#############################################################


#######################################
    def file_path(self, ):

        #self.input_pth = basepath+'/data/in'


        # 0 -> default: simu-results file in data/in
        # 1 -> data from par
        # 2 -> existing materialbalance
        # 3 -> external file-source (path from pars OR browse)
        # 4 -> ??? from sig-df ->> SIMPEL

        return



    '''

    def mk_fl_pth(self):
        ### create storga path for material balance
        self.sto_fl_pth = (self.glbPar.pth +'/'
        +self.glbPar.sto_dirnm+'/'
        +'Mat_'+self.glbPar.sto_flnm+'.csv')
        ### create storga path for TEA results
        return

    '''

    def browse_pth(self):

        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window

        #currdir = os.getcwd()
        tempdir =0
        '''
        filedialog.askdirectory(parent=root, initialdir=, title='Please select a directory')
        '''

        if len(tempdir) > 0:
            #print("You chose %s" % tempdir)
            pth_out = tempdir
        else:
            pth_out = None
        return pth_out

    def read_sourcedata(self, path_to_file, specs=None):
        sim_data = None
        return sim_data





    def check_format():
        '''
        check format of matbal-dataset (df)
        input df must contain:
        date        | n_H2      | n_O2      | n_H2O     | P_in   | P_act
        pd.datetime | in mol/s  | in mol/s  | in mol/s  | in kW  |  in kW  |
        '''
        return


    def group_by_year(self):
        '''
        if multiple years clc
        df must contain datetime-column: 'time' (not index)

        #TODO: check order !
        '''

        ### group df by years
        df['year'] = df.time.dt.to_period('Y')
        grpd = df.groupby(df.year)

        ### make list of dfs for every year
        dflst = []
        for item in grpd:
            dflst.append(item[1])

        return

    def selectsource(self):
        '''
        select source of data for running TEA on

        return: filelist

        - sngl/ multiple files ?
        - multiple yrs ?

        - files in dir?
        - matbal-files in dir?
        - name keys?

        '''


        if not ((self.basic_par['pth'] == 'NOpath')
        or ('default' in self.basic_par['pth']) ):

        # os.path.isfile() // os.path.isdir()
            for pth_i in pth_lst:
                # check for existing file
                flnmi = os.path.splitext(os.path.basename(path))[0]
                mb_flnmi = 'MAT_BAL_'+flnmi
                mb_exists = self.check_existance(dirnm='data/mat', key=flnm)
                # to list


            if materialbalance_file_existing:
                from_matbal = True
            '''
            if ?:
                from_path = True
            '''
            if 'materialbalance_results_' in flnms:
                pass

        else:
            file_source = 'default' # default directory: data/in

        # decide if multiple True


            print('input- path: ', self.input_pth)
        ######################################################
        src = self.basic_par.lower()
        try:
            int_src = int(src)
        except:
            int_src = None

        # 4 -> from sig-df
        if (src == 4) or ('simpel' in src):

            print(' -- running simpEL as source -- ')
            print(' source-directory: ', self.sto_fl_pth)
            self.mk_fllst()
            if not self.fllst:
                print(' +++ no files found +++')
            else:
                self.data_src_nm = 'fllst'


        elif (int_src == 3) or ('ext' in src):
            print(' -- browse external file -- ')
            pth = self.browse_pth()

        elif (int_src == 2) or ('int' in src):

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


        elif (src == 0) or ('default' in src):

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


    def read_file(pth, ucols=None, cols_to_try=None):
        ''' read files from given path
        try different types of separators (, and ;)
        try different column-lists
        return df
        '''
        #TODO: try/except does not ensure correct choice of separator !!!


        #TODO: set variable for avoiding recursive tests

        if cols_to_try:
            fcols = ucols.copy()
            fcols= fcols.extend(cols_to_try)
            try:
                try:
                    df = pd.read_csv(pth, usecols=fcols)
                except:
                    df = pd.read_csv(pth, sep=';',decimal=',', usecols=fcols)
            except:
                try:
                    df = pd.read_csv(pth, usecols=ucols)
                except:
                    df = pd.read_csv(pth, sep=';',decimal=',', usecols=ucols)
        else:
            try:
                df = pd.read_csv(pth)
            except:
                df = pd.read_csv(pth, sep=';',decimal=',')
        return df

    def clean_df(df, P_max=0, vw_max = 0, ):
        '''
        clean df
        yielding inly valid values
        '''

        for coli in df.columns:
            if 'P' in coli:
                df[coli] = np.where(df[coli]<=P_max*1.3,df[coli],0)
            elif 'v' in coli:
                df[coli] = np.where(df[coli]<=vw_max*1.3,df[coli],0)
        return df

    def rename_columns(df):
        '''
        rename columns if df based on ...?
        adopted from py_scripts_v101.processdata.aux.read
        '''
        ncols=[]
        #cols = df.columns

        if 'Unnamed: 0' in df.columns:
            df = df.drop(['Unnamed: 0'], axis = 1) # drop column
        cols = df.columns
        wind_list = ['vw', 'v_w','wind'] #possibkle column names for wind velocity
        pow_list = ['P', 'Leistung','power'] #possibkle column names for plant power
        dat_list = ['Datum', 'Date']
        #TODO: what about max/min ?
        w_mimx = [[],[]]
        p_mimx = [[],[]]
        w_idx = []
        p_idx = []
        new_cols = []
        w_cnt = 0
        p_cnt = 0
        dat_cnt=0
        for i,col in enumerate(cols):
            if any([ele for ele in wind_list if(ele in col)]):

                w_idx.append(i)

                if len(col.split(' '))>1:
                    if 'min' in col.lower():
                        w_mimx[0].append(i)
                        new_cols.append('vW_'+str(w_cnt)+'_min')
                    elif 'max' in col.lower():
                        w_mimx[1].append(i)
                        new_cols.append('vW_'+str(w_cnt)+'_max')
                else:
                    w_cnt+=1
                    new_cols.append('vW_'+str(w_cnt)+'_')

            elif any([ele for ele in pow_list if(ele in col)]):
                p_idx.append(i)

                if len(col.split(' '))>1:
                    if 'min' in col.lower():
                        p_mimx[0].append(i)
                        new_cols.append('P_'+str(p_cnt)+'_min')
                    elif 'max' in col.lower():
                        p_mimx[1].append(i)
                        new_cols.append('P_'+str(p_cnt)+'_max')
                else:
                    p_cnt +=1
                    new_cols.append('P_'+str(p_cnt)+'_')

            elif any([ele for ele in dat_list if(ele in col)]):

                if dat_cnt >0:
                    strng = 'Date '+str(dat_cnt)
                else:
                    strng = 'Date'
                new_cols.append(strng)
            else:
                new_cols.append(col)
            dat_cnt +=1
        #col_arr = np.array(cols)
        #w_ele =

            #bool_answ = any(ele in col for ele in test_list)
        #TODO what, if more than one col?
            #if
        prnt_lst = [w_mimx, p_mimx, w_idx, p_idx]
        nm_lst = ['w_mimx', 'p_mimx', 'w_idx', 'p_idx']
        for i,ele in enumerate(prnt_lst):
            print(nm_lst[i]+': ', ele)
        print('old: ', cols)
        print('new cols: ', new_cols)
        #return
        df.columns = new_cols
        return df

################################################################################

def extr_data_properties(parfiles):
    '''
    read parfiles and collect data/properties accordingly
    '''
    prop_dct={}
    for pfl in parfiles:
        dct = {}
        dct['flnm_prms']=pfl
        ppth = os.path.dirname(pfl)
        # prm = rf.read_json_file(pfl)
        with open(pfl) as jsonfile:
            prm0=json.load(jsonfile)
        tag = prm0.get('tag_sim', None)
        if tag is not None:
            prm = prm0.get('parameters', {})
            dct['prm0'] = prm0
            dct['pth_out'] = ppth
            dct['name'] = prm.get('scen_name', None)
            dct['pth_sig'] = prm.get('relpth_sig_data', None)    # Path to Sig-File
            bsc_par = prm.get('bsc_par', None)
            if bsc_par is not None:
                dct['tec_el'] = bsc_par.get('tec_el', None)    # electrolysis technology
                dct['tec_gen'] = bsc_par.get('tec_ee', None)    # RE technology

                dct['rpow_el'] = bsc_par.get('rpow_el', None)     # nominal power of electrolysis plant
                dct['rpow_gen'] = bsc_par.get('rpow_ee', None)     # nominal power of re plant
                # 'npf': None,    # fraction of nominal renewable power input
            #'files': None,
            dct['res_lst'] = mk_filelist(ppth, skey=tag+'*results*',  sffx='.csv')
            dct['matbal_lst'] = mk_filelist(ppth, skey=tag+'*matbal*',  sffx='.csv')
            dct['else_lst'] = mk_filelist(ppth, skey=tag+'*',
                                            sffx='.csv',
                                            exclude=['matbal','results'])
            ## read df-heads
            spc_lst = []
            df_lst = []
            for fl in dct['res_lst']:
                specs,df = read_data_df(fl,ini=True)
                spc_lst.append(specs)
                df_lst.append(df)
            dct['res_specs'] = spc_lst
            # dct['res_df'] = spc_lst
            dct['years'] = get_simu_years(prm)
            dct['files'] = dict(zip(dct['years'],dct['res_lst']))
            prop_dct[tag]=dct
    return prop_dct

def mk_filelist(pth, skey=None, primwc=False, sffx='', exclude=[]):

    if skey is None:
        skey='*'
    if sffx is not None:
        skey += sffx
    if primwc:
        skey =  '*'+skey
    spth = os.path.join(pth,skey)
    print('spth: ', spth)
    fllst = glob.glob(spth)
    print('fllst (mk_filelist(0): ', fllst)
    lst_o = []
    for fl in fllst:
        if exclude:
            for key in exclude:
                if key not in fl:
                    lst_o.append(fl)
        else:
            lst_o.append(fl)
        # lst_o += [fl for key in exclude if key not in fl]
    print('fllst (mk_filelist(1): ', lst_o)
    return lst_o

def get_simu_years(prms):
    '''
    Extract years of actual simulation
    either from actual dates,
    or from parameters (main or sig-metadata)
    '''

    dates = []
    # prms = dct_par.get('parameters', None)
    if prms is not None:
        sig_med = prms.get('metadata_sig', None)
        sd_sig = sig_med.get('start_date', None)
        ed_sig = sig_med.get('end_date', None)
    sd_main = prms.get('date_start', None)
    ed_main = prms.get('date_end', None)
    sd_act = prms.get('date_start_act', None)
    ed_act = prms.get('date_end_act', None)
    if (sd_act is None):
        sd_lst = [date for date in [sd_sig, sd_main] if date is not None]
        sd_lst.sort()
        sd_act = sd_lst[0]
    if (ed_act is None):
        ed_lst = [date for date in [ed_sig, ed_main] if date is not None]
        ed_lst.sort()
        ed_act = ed_lst[0]
    yr_s = pd.to_datetime(sd_act).year
    yr_e = pd.to_datetime(ed_act).year
    if yr_s < yr_e:
        yrs = list(np.arange(yr_s, yr_e+1))
    elif yr_s > yr_e:
        yrs = list(np.arange(yr_e, yr_s+1))
    else:
        yrs = [yr_s]
    return yrs

def mk_abspath(basepath='', tar='', cat=None):

    if tar[0]=='/':
        tar = tar[1:]
    ### mat
    if 'mat' in cat:
        relpth = 'data/mat/'
    ### data
    elif 'data' in cat:
        relpth = 'data/out/'

    elif not cat:
        relpth = ''

    return os.path.join(basepath, relpth, tar)

def mk_dir(abspth, dirnm=None):
    if not os.path.exists(abspth):
        os.mkdir(abspth)
        print(f'...creating directory: {abspth}')
    return

def df_to_dct(df_in, idx_col=None):
    '''
    return dict from df
    '''
    df = df_in.copy()
    if idx_col:
        df = df.set_index(idx_col)
    list(df_in.itertuples(name='Row', index=False))

    return


def input_scen_file(self,):
    ### select paths to search in
    pths = [os.path.dirname(self.fllst[0])]
    if not self.par['basic']['root_dir_of_files']:
        pths.append('/')
    else:
        pths.append(self.par['basic']['root_dir_of_files'])
    res = find_files(self.tag, pths)
    lst = []
    for fl in res:
        if '_parameters' in fl:
            lst.append(fl)

    if len(lst) >1:
        idx = input(f'Which of the following scenario-files is valid? {lst}')
    else:
        idx = 0
    try:
        with open(lst[int(idx)]) as jsonfile:
            data=json.load(jsonfile)
    except:
        data = None

    return data

def find_files(search_key, paths=[]):
    for pth in paths:
        result = []
        for root, dirs, files in os.walk(pth):
            #print(root, dirs, files)
            for fl in files:
                if search_key in fl:
                    result.append(os.path.join(root,fl))
    return result

def read_data_df(fl, ini=False):
    print('Reading file: ', fl)
    dct, df_skpr = read_specs(fl)
    print('df_specs: ', dct)
    print('df_skpr: ', df_skpr)
    #dct['df'] = pd.read_csv(fl,skiprows=(df_skpr), parse_dates=[0])
    if ini:
        dff = pd.read_csv(fl,skiprows=(df_skpr), index_col=[0], nrows=10) # REad only slice of df (read in full df later in simuinst)
    else:
        dff = pd.read_csv(fl,skiprows=(df_skpr), index_col=[0])
    return dct, dff

def read_specs(filepth):
    '''
    read files and extract specs, data

    -- check, if matbal exists
    '''
    filename = os.path.splitext(os.path.basename(filepth))[0]
    skpl = get_line(filepth, search_text='begin Simu - metadata') # get last line (number) of specs
    line = get_line(filepth) # get last line (number) of specs
    df_sl = get_line(filepth, search_text='begin Simu - data') # number of lines to skip for df reading
    print('line: ', line)
    print('skpl: ', skpl)
    if line:
        d_in = pd.read_csv(filepth, index_col=0,skiprows=skpl, nrows=line-skpl-1, header=None).T.to_dict('records')[0]
        d_specs = {}
        for key, val in d_in.items():
            #print('key:', key)
            strpkey = key.strip()
            #print('strpkey: ', strpkey)
            #print('strpval: ', val.strip())
            #if strpkey != key:
            #del d_specs[key]
            #d_specs[strpkey] = val.strip()
            if isinstance(val, str):
                d_specs[strpkey] = val.strip()
        ### -> reading data only, if not matbal (in elSimu-instances)
        df_data = None #pd.read_csv(filepth, index_col=0, skiprows=line)
        #tag = d['tag']
        #full_dict = d_spec.copy()
        #full_dict['dfs']
    else:
        # no specs in csv
        '''
        str_elem = filename.split('_') # split by _
        if str_elem[-1] != '':  # if last char is '_', last elem in list will be ''
            strn = -1
        else:
            strn = -2
        ### CAUTION: find returns ambigous vals e.g. with dates
        #tag = filename[:filename.find(str_elem[strn])] #use filename without yr-string as tag
        '''
        print('CAUTION: hardcoded filename-splitting')
        tag = filename[:51]
        print('---<->>>>> filename[:-51]: ', filename[:-51])

        lst = []
        gen_tec_keys = ['WEA', 'PV']
        sig_subkeys = ['off', 'on']
        gen_plant_type = None #?
        tec_keys = ['PEM', 'AEL']
        npf_keys = ['04', '06', '08']
        nomp_keys = ['']
        searchlist = [gen_tec_keys, tec_keys, npf_keys, nomp_keys]
        key_lst = ['gen_tec', 'el_tec', 'scl', 'nomp']
        #TODO: d_speca from defaultdict?
        d_specs = self.def_dict.copy()
        #print('d_specs:', d_specs)
        d_specs['tag'] = tag
        for s_key, keylst in zip(key_lst, searchlist):
            for key in keylst:
                if key in filename:
                    d_specs[s_key] = key

        #d_specs = self.specs_from_flnm()
        #TODO: check, if full reading can be avoided
        df_data = pd.read_csv(filepth)
        #print(df_data.head())
        #TODO: check year in datetime column
        cols = df_data.columns

        for cnm in cols:
            if 'Unnamed' in cnm:
                df_data = df_data.drop(cnm, 1)
            if ('date' in cnm.lower()) or ('datum' in cnm.lower()):
                #yr = df_data[cnm].dt.to_period('Y') # does not return single value
                y = [x.year for x in df_data[cnm].dt.to_period('Y').tolist()]
            else:
                print('no specs of date in df...')
                y = str(self.yr_cnt)
                self.yr_cnt += 1

        y_un = self.unique_list(y) # return unique objects
        if len(y_un)>1:
            print('more than 1 year in df....????')
            print('file:', filename)
            d_specs = None
        else:
                #df_data.time.dt.to_period('Y')
            yr_strng = str(y_un)
            d_specs['name'] = filename # remove yr-ending (int)?
            d_specs['yrs'] = yr_strng #[yr_strng]
            d_specs['files'] = os.path.basename(filepth) #{yr_strng : filename}
            d_specs['dfs'] = df_data #{yr_strng : df_data}
        #print('d_specs', d_specs)
        d_specs['full_flpth'] = filepth
    return d_specs, df_sl#, df_data

def get_line(filepth, search_text='end Simu - metadata', num_end=100):
    '''
    get line in csv, containing the search-string (default)
    or any specified search text
    '''
    with open(filepth, 'r') as f:
        for num, line in enumerate(f,1):
            if search_text in line:
                return num
            if num > num_end:
                return None

    '''
    def check_multiyr(self, fllst, sep='_', num=1):
        ''''''
        check, if multi-year file set exists
        and
        ''''''

        multi_yr = []
        for fl in fllst:
            fflnm = os.path.splitext(fl)[0]
            splt = fflnm.rsplit(sep, num)
            while not splt[-1]:
                num += 1
                splt = fflnm.rsplit(sep, num)
            #[flnm, yr] = splt
            multi_yr.append(splt)
            num = 1
        return multi_yr
    '''

class handleOutputFiles():

    def __init(self):
        self.output_path = None
        self.filename_materialbalance = None
        self.filename_teco_results = None

    def create_logfile(obj):
        for att in obj.__dict__:
            print(att,': ', getattr(obj,att))

        return

def prnt_fllst(fllst, name='NoName'):
    '''


    Parameters
    ----------
    fllst : TYPE
        DESCRIPTION.
    name : TYPE, optional
        DESCRIPTION. The default is 'NoName'.

    Returns
    -------
    None.

    '''

    print(f'Filelist [{name}] contains the following files: ')
    for i,fl in enumerate(fllst):
        print(f'[{i}] ->|  ', fl)
    return

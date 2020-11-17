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
    def __init__(self, basepath, params):

        self.basepath = basepath
        self.yr_cnt = 0
        self.basic_par = params.cont.basic
        self.fllst = self.mk_fllst() # make list of files (fullpath) containing simudata or sigdata
        self.def_dict = self.ini_dict()
        self.list_of_dicts = self.files_to_dicts(self.fllst)
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
        fllst_raw = self.search_files(dirnms = self.basic_par['directory_names'],
                                        key = self.basic_par['selection_keys'])

        if not self.basic_par['manual_file_selection']:
            return fllst_raw
        else: #(additional) manual selection
            ### -- select files ?
            for num, fl in enumerate(fllst_raw):
                print(num,'->', fl)
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
            dct, df_skpr = self.read_specs(fl)
            #print('df_skpr: ', df_skpr)
            #dct['df'] = pd.read_csv(fl,skiprows=(df_skpr), parse_dates=[0])
            df = pd.read_csv(fl,skiprows=(df_skpr), index_col=[0])
            #print('df: ', df.head())
            #df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d HH:%MM:%SS')
            df['date'] = pd.to_datetime(df['date'],unit='ns')
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
                print('fl:', fl)
                if not key:
                    fllst.append(fl)
                elif len(key)>1:
                    if key[num] in fl:
                        fllst.append()
                else:
                    if key in fl:
                        fllst.append(fl)

        return fllst # return list of files in dir (fullpath)

#############################################################

    def get_line(self, filepth, search_text='end Simu - metadata', num_end=100):
        '''
        get line in csv, where ist says 'end info' (default)
        or any specified search text
        '''
        with open(filepth, 'r') as f:
            for num, line in enumerate(f,1):
                if search_text in line:
                    return num
                if num > num_end:
                    return None


    def read_specs(self, filepth, ):
        '''
        read files and extract specs, data

        -- check, if matbal exists
        '''
        filename = os.path.splitext(os.path.basename(filepth))[0]
        skpl = self.get_line(filepth, search_text='begin Simu - metadata') # get last line (number) of specs
        line = self.get_line(filepth) # get last line (number) of specs
        df_sl = self.get_line(filepth, search_text='begin Simu - data') # number of lines to skip for df reading
        #print('line: ', line)
        #print('skpl: ', skpl)
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

class handleOutputFiles():

    def __init(self):
        self.output_path = None
        self.filename_materialbalance = None
        self.filename_teco_results = None

    def create_logfile(obj):
        for att in obj.__dict__:
            print(att,': ', getattr(obj,att))

        return

class handleParams():
    '''
    select version of parameter sets
    read and convert each to df
    '''
    #TODO: enable parameter input via xls
    #TODO: add descriptive text in json files ?

    def __init__(self, basepath):
        self.lst_parfiles = glob.glob(basepath+'/par/*.json')

        #print(self.lst_parfiles)
        self.print_filelist(self.lst_parfiles, name='Parameter')
        self.parameter_version = self.select_par_version()
        self.ntpar = self.read_params(basepath)

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

            #df_par.append(self.json_to_df(jsonpth))
            #print(jsonpth)
            with open(jsonpth) as jsonfile:
                data=json.load(jsonfile)
                #print(data)
                df_par.append(data)



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

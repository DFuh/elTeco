'''
main script
define classes for economical assessment and simulation results
run tea
'''
import sys
import os
import glob
from .auxf.mainclasses import elEco#, elSimu
from .auxf import handlefiles as hfs
'''
def mainrun():
    tea_inst = elEco()
    run=True
    while run:
        run = input('rerun? [y/n]').lower()==y
    return
'''

# pass variable with call:
#https://stackoverflow.com/questions/18742657/execute-shell-script-from-python-with-a-variable
#???

#TODO: where to specify columns for materialblance? // or
#TODO: several instances for more than 1year?

#TODO: if list in basic_params

#TODO: plotting

def mk_fllst(pth_to_dir, searchstring, skip_dir_level=1, sffx='',
                str_filter='', exclude=[], print_lsts=False):

    ### Search files
    # lst = glob.glob(inp+'/*/*matbal*ext_2208*.csv')
    str_skp = '*/' * skip_dir_level
    sstrng = pth_to_dir+'/'+str_skp+searchstring+sffx
    lst = glob.glob(sstrng)

    ### Apply filter
    if str_filter !='':
        lst = [item for item in lst if str_filter in item]

    ### Exclude
    for excl_key in exclude:
        lst = [item for item in lst if excl_key not in item]
        exlst = [item for item in lst if excl_key in item]
        if print_lsts:
            print('Items in Exclude-List: \n')
            for item in exlst:
                print(item)
            print('items in list: \n')
            for item in lst:
                print(item)

    n = len(lst)
    print(f'{n} files found for: ', sstrng)
    return lst


def mk_tea_instances(fllst, addstrng_flnm_teares='',
                    select_parameter_version=True):

    lst_instances = []
    for j,sf in enumerate(fllst):
        print(f'[{j}] ->| ', sf)
    slct = input('Add Simulation? (Enter-> all/ int0,int1 / n:any key): ')
    if slct=='':
        fltrd_lst = fllst
        skip = False
    else:
        try:
            skip = False
            slct_lst = [int(item) for item in slct.split(',')]
            fltrd_lst = [fllst[item] for item in slct_lst]
        except:
            print(' -- Invalid input -- ')
            skip = True

    if not skip:
        for fli in fltrd_lst:
            tea_inst = elEco(pth_data_loc=os.path.dirname(fli),
                                flnm_matbal=fli,
                                addkey_flnm_teares=addstrng_flnm_teares,
                                slct_par_version=select_parameter_version)
            lst_instances.append(tea_inst)
    else:
        print(' - skip -')
        lst_instance=[]

    return lst_instances


def run_tea_inst(lst_inst):

    n = len(lst_inst)
    print(f' --- Run tea for {n} instances --- ')
    for i,inst in enumerate(lst_inst):
        print(f' ... |-> run tea-{i}/{n} ')
        inst.setup_tea_sim()
        inst.run_tea()
    print( ' --- finish ---')


    return

if __name__ == '__main__':
    #mainrun()
    print('...run...')
    # inp = input('Please insert dirname: ')
    # inp = '/home/dafu_res/01_data/epos_calc_out/main_runs_202203/20220312'
    if False:#True:
        pass
        #inp = '/home/dafu_res/01_data/epos_calc_out/main_runs_202205/20220430'
        #if inp !='':
        #    sdir = inp
        #    dirs = os.walk(sdir)
            # bpth = dirs[0]
        #n=0
        #for root,dir,fls in dirs:
        #    if root == inp:
        #        for dirnm in dirs:
        #            print('dirnm: ', dirnm[0])
        #            inpi = input(f'Apply for {dirnm[0]} (y/ any key)')
        #            if 'y' in inpi.lower():
        #                tea_inst = elEco(pth_data_loc=os.path.join(root,dirnm[0]))
        #                #tea_inst.run_tea()
    if True:
        print(sys.argv)
        if len(sys.argv)>1:
            inp = str(sys.argv[-1])
        else:
            inp = input('Please insert dirname: ')

        print('Dir-Input: ', inp)
        #dirlst = []
        #for (root,dirs,files) in os.walk(inp):
        #    [dirlst.append(os.path.join(root,item)) for item in dirs]


        #lst = []
        #dirlst = glob.glob(inp)
        #hfs.prnt_fllst(dirlst, 'DirList')
        #print('dirlst: ', dirlst)
        #for dir_ in dirlst:
        #    [lst.append(item) for item in glob.glob(os.path.join(dir_,'*matbal*ext_2208*.csv'))]
        lst = glob.glob(inp+'/*/*matbal*ext_2208*.csv')

        fltr = input('Enter Filter for list: (skip: Enter)'+sffx)
        if str_filter !='':
            lst = [item for item in lst if str_filter in item]

        #hfs.prnt_fllst(lst, 'Fllst')
        #hfs.prnt_fllst(lst2, 'Fllst 2')
        print(' --- --- ---')
        for j,sf in enumerate(lst):
            print(f'[{j}] ->| ', sf)
            slct = input('Run Simulation? (y:Enter/ n:any key): ')
            if slct=='':
                tea_inst = elEco(pth_data_loc=os.path.dirname(sf))
                tea_inst.setup_tea_sim()
                tea_inst.run_tea()
    else:
        tea_inst = elEco()
        tea_inst.run_tea()
    #for num,inst in enumerate(tea_inst.simuinst):

        #print('num: ', num)
        #inst.
        #print('{} --->{}\n{}'.format(num, inst.name,inst.file_list))
        #print('root-dir: ', inst.basepath)
        #print('pth_list: ', inst.pth_lst)

    #print(tea_inst.Parameters.dfs.basic.dirname)
    #dat_inst = elSimu()

'''
main script
define classes for economical assessment and simulation results
run tea
'''
import os
import glob
from auxf.mainclasses import elEco#, elSimu
#import aux.handlefiles as hfs
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
        inp = input('Please insert dirname: ')
        lst = glob.glob(os.path.join(inp,'*matbal.csv'))

        fltr = input('Enter Filter for list: (skip: Enter)')
        if fltr !='':
            lst = [item for item in lst if fltr in item]

        for j,sf in enumerate(lst):
            print(f'[{j}] ->| ', sf)
            slct = input('Run Simulation? (y:Enter/ n:any key): ')
            if slct=='':
                tea_inst = elEco(pth_data_loc=os.path.dirname(sf))
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

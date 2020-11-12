'''
main script
define classes for economical assessment and simulation results
run tea
'''
from aux.mainclasses import elEco, elSimu
import aux.handlefiles as hfs 
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
    tea_inst = elEco()
    for num,inst in enumerate(tea_inst.simuinst):
        print('{} --->{}\n{}'.format(num, inst.name,inst.file_list))
        print('root-dir: ', inst.basepath)
        print('pth_list: ', inst.pth_lst)

    #print(tea_inst.Parameters.dfs.basic.dirname)
    #dat_inst = elSimu()

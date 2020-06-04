'''
main script
define classes for economical assessment and simulation results
run tea
'''
from aux.ino import elEco, elSimu



if __name__ == '__main__':
    tea_inst = elEco()

    print(tea_inst.Parameters.dfs.ec)
    #dat_inst = elSimu()

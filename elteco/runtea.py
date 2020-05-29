'''
main script
define classes for economical assessment and simulation results
run tea
'''
import aux.handlefiles as hf
import aux.materialbalance as amb
import aux.teconas as tea

### define main
class elEco(object):
    """main class elEco."""

    def __init__(self, arg):
        #super(elEco, self).__init__()
        self.arg = arg

        #TODO# read parameter file

        self.get_mat_data = self.sw_src(self.data_src_nm)


    def run_teco(self):
        print('...run teco...')
        #check_mat_data(self)

        ### prepare files

        ### provide material data

        ### techno-economical assessment

        ### data output

        ### data visualization

        self.mk_fl_pth()
        #TODO: check, if mat-df exists: override or new flnm?
        self.cc_data_source()

        self.get_mat_data()
        self.mk_mat_df()

        self.clc_eco()

        self.mk_full_df()

        return

class elSimu(object):
    """docstring for elSimu."""
    ''' instances of simulation-results'''

    def __init__(self, arg):
        #super(elSimu, self).__init__()
        self.arg = arg



if __name__ == '__main__':

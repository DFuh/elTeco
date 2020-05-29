'''
main script
### ###
'''
import aux.handlefiles as hf
import aux.materialbalance as amb
import aux.teconas as tea

### define main
class EL_Eco(object):
    """main class EL_Eco."""

    def __init__(self, arg):
        #super(EL_Eco, self).__init__()
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

class EL_Simu(object):
    """docstring for EL_Simu."""
    ''' instances of simulation-results'''

    def __init__(self, arg):
        #super(EL_Simu, self).__init__()
        self.arg = arg



if __name__ == '__main__':

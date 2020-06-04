'''
main classes
output plot ?
'''
import os
import aux.handlefiles as hf
import aux.materialbalance as amb
import aux.teconas as tea

### define main
class elEco():
    """main class elEco."""

    def __init__(self, *args):
        #super(elEco, self).__init__()
        #self.arg = arg
        self.basepath = os.getcwd()
        #TODO: decide, wether df or dict !
        self.Parameters = hf.handleParams(self.basepath)

        #self.get_mat_data = self.sw_src(self.data_src_nm)
        #TODO: consider multiple par-tecos

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

'''
function in EL_Teco
handle files for ...
'''

### main handling function
def prepare_files():

    # create path to ...???
    mk_fl_pth()

    # choose data source (material balance) for calculation


    return




#######################################
def mk_fl_pth(self):
    self.sto_fl_pth = self.glbPar.pth+'/'+self.glbPar.sto_dirnm+'/'+'Mat_'+self.glbPar.sto_flnm+'.csv'
    return

def cc_data_source(self):
    '''
    ???
    '''
    src = self.glbPar.choose_source
    if src == 0:
        print(' -- using simulation-files as source -- ')
        print(' source-directory: ', self.sto_fl_pth)
        self.mk_fllst()
        if not self.fllst:
            print(' +++ no files found +++')
        else:
            self.data_src_nm = 'fllst'

    elif src == 1:
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
    return

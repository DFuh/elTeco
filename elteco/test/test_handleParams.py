'''
test of parameter file handling
class : handleParams()
'''

#from ..aux import handlefiles as hf

if __name__ == '__main__':
    if __package__ is None:
        import sys
        import os
        sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
        from aux import handlefiles as hf
    else:
        from ..aux import handlefiles as hf

    #cwd = os.getcwd()
    #print('cwd:',cwd)
    bpath = '/home/dafu_res/0_modeling/Projects/elTeco/elteco'
    hP = hf.handleParams(bpath)

'''
further auxilliaries (utils?)
'''
import sys
import logging

def ini_logging(obj, name=None):
    print('obj in ini_logging: ', obj)

    if not hasattr(obj, 'name'):
        nm = name
    else:
        #nm = str(obj[0].tdd)+'_'+obj[0].name
        nm = '-->| '+ obj.name + ' |<--'
    logging.root.setLevel(logging.DEBUG)
    log = logging.getLogger('lggr_'+nm)
    formatter =logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')#,

    fh = logging.FileHandler(filename=nm+'.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return logging, 'lggr_'+nm

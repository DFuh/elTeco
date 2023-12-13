'''
further auxilliaries (utils?)
'''
import os
import sys
import logging


def ini_logging(obj, name=None, pth=None, notest=True):
    print('obj in ini_logging: ', obj)
    if not obj:
        nm = name
    else:
        nm = str(obj.today_ymdhs)+'_'+obj.name
    if notest:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    #logging.root.setLevel(logging.DEBUG)
    log = logging.getLogger('lggr_'+nm)
    formatter =logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s %(name)s \n- %(message)s')#,

    if not pth:
        pth=''
        # fh = logging.FileHandler(filename=nm+'.log')
    # else:
    lgpth = os.path.join(pth, 'logfiles')
    if not os.path.exists(lgpth):
        print('Make logpth: ',lgpth)
        os.makedirs(lgpth)
    flnm = os.path.join(lgpth,nm+'.log')

    if not hasattr(obj, 'logger'):
        obj.logger = log
    if not obj.logger.handlers:
        fh = logging.FileHandler(filename=flnm, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log, 'lggr_'+nm # old: return logging, 'lggr_'+nm


def ini_logging_prev(obj, name=None):
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

    return log, 'lggr_'+nm

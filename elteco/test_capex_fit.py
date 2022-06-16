'''
test capex function based on Proost2019

--> move to "test" directory !

'''
import numpy as np
import matplotlib.pyplot as plt

from auxf.mainclasses import elEco, elSimu
import auxf.teconas as tea

def efun(x, a, b, c):

    return a * np.exp(b/x) + (c*x)

def CAPEX_fit(P_in,tec):
    ''' curvre-fit data based on Proost2019, fig3,fig4 '''
    '''AEL -> 0 || PEM -> 1 '''
    llmt = [2.1,0.7] # Lower limit of plant power // in MW
    k_lmt = [400,545] # Lower limit of specific investment cost in €/MW
    linf = [[[0.4,2000],[2,500]], [[0.2,3000],[0.6,2000]]] # Linear fit for AEL linf[0] and PEM linf[1] in low power range

    # Extracted values from Proost2019 (Figure 4)
    # Might be checked...
    aa,bb,cc = np.array([   [582.609751, 0.367851704, -1.03609829], # AEL
                             [737.069812, 0.375146694, -13.7710513] # PEM
                         ])[tec]
    # Linear regression in low power range
    if P_in < llmt[tec]:
        k_spec = P_in*((linf[tec][0][1]-linf[tec][1][1]) / (linf[tec][0][0]-linf[tec][1][0]))+linf[tec][0][1]
        #print('P_in:',P_in,'k_spec',k_spec)
        add_klmt_ael = 689 # additional lower cost limit for AEL, based on Fig 3 (bend between single and multistack (?))
        if (tec == 0) & (k_spec < add_klmt_ael):
            k_spec = add_klmt_ael
    else:
        k_spec = efun(P_in,aa,bb,cc) # Calc specific cost based on fitted function
    if k_spec < k_lmt[tec]: # Apply lower cost limit
        k_spec = k_lmt[tec]
    return k_spec


def test_cf(tec, p_val=None):
    if tec.lower() == 'ael':
        tecint=0
    elif tec.lower() == 'pem':
        tecint=1
    else:
        print('no valid tec name')
    if not p_val:
        p_val = np.linspace(0.1, 150, 500) # P in MW
        capex = np.zeros(len(P_val))

        for k in range(len(P_val)):
            capex[k] = CAPEX_fit(P_val[k], tecint)
    else:
        capex = CAPEX_fit(p_val, tecint)

    return p_val, capex


def testplot(x_arr, y_arr, ref_arr):

    plt.figure()
    plt.scatter(x_arr, y_arr, label='testplot_capex')
    plt.scatter(x_arr, ref_arr, label='ref_capex')
    plt.legend()
    plt.show()
    return

if __name__ == '__main__':


    test_instance = elEco(test=True)
    pv = np.zeros(len(test_instance.simuinst))
    cv = np.zeros(len(pv))
    k_spec = np.zeros(len(pv))
    for n, inst in enumerate(test_instance.simuinst):
        ### make ref values
        pv[n], cv[n] = test_cf(inst.tec_el, p_val=float(inst.el_pwr_nom))
        ### calc value in inst
        k_spec[n] = tea.capex_fit(inst, float(inst.el_pwr_nom), inst.par['teco_'+inst.tec_el]) #tec specific parameters | dict)

    testplot(pv, k_spec, cv)

    print('... AEL capex test ...')
    print(' --- not implemented yet ---')

    print('... PEM capex test ...')
    print

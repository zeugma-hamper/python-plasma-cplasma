from cplasma.native import Hose, Gang, PlasmaException
from pprint import pprint

def main():
    gang = Gang()
    for poo in Hose.listPools():
        gang.join(poo)

    try:
        while True:
            pro, ts, idx, pool = gang.awaitNext()
            print('# %s\t%f\t%d' % (pool, ts, idx))
            pprint(pro.emit())
            print('...')
    except PlasmaException, pe:
        print(pe.description)

    

if '__main__' == __name__:
    main()

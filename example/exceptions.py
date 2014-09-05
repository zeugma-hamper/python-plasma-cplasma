from cplasma.metabolizer import Metabolizer
from cplasma.exceptions import PlasmaException

if '__main__' == __name__:
    metabo = Metabolizer()

    try:
        metabo.poolParticipate('FAKE')
    except Exception as pe:
        #Some notes:
        print('Plasma Exception 1 - type:%s / msg: %s' % (type(pe), pe))

    try:
        metabo.poolParticipate('FAKE')
    except PlasmaException as pe:
        #Some notes:
        print('Plasma Exception 2 - type:%s / msg: %s' % (type(pe), pe))

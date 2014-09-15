from cplasma.metabolizer import Metabolizer
from cplasma.exceptions import PlasmaException
from pprint import pprint

if '__main__' == __name__:
    metabo = Metabolizer()
    metabo.poolParticipate('sluice-to-heart')

    def on_heartbeat(p):
        ing = p.ingests.emit()
        print('The time is %f' % ing['time']['current'])

    metabo.appendMetabolizer(['sluice', 'prot-spec v1.0', 'psa', 'heartbeat'],
                             on_heartbeat, 'heartbeat')

    try:
        metabo.metabolize()
    except PlasmaException as pe:
        print('Plasma Exception: %s' % pe.description)

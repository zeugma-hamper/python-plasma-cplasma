# (c) 2014 MCT

import sys
from cplasma.metabolizer import Metabolizer

if '__main__' == __name__:
    pools = sys.argv[1:]
    if 1 > len(pools):
        print('Usage: %s pool1 [pool2 ...]' % sys.argv[0])
        sys.exit(0)
    metabo = Metabolizer()
    for pool in pools:
        metabo.poolParticipate(pool)
    
    def dump(p):
        print(p.toYaml())
    
    metabo.appendMetabolizer([], dump, 'everything')

    metabo.metabolize()

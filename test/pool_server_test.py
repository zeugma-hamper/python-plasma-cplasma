import unittest
import os.path

#Make sure the test uses the local cplasma instead of the global one
#Do this because this is a library and is very frequently already installed
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cplasma
from cplasma import Hose, Protein
from cplasma import yamlio


TEST_POOL = 'temp-pool-test'


class TempPool(object):
    """
    Create a temporary pool & hose
    TODO: Might want this in cplasma/pyplasma
    """
    def __init__(self, pool_name):
        try:
            #Create a pool
            Hose.create(pool_name, 'mmap', {'size': 10*1024*1024})
            self._created = True
        except cplasma.exceptions.PoolExistsException as exc:
            self._created = False
        self._pool_name = pool_name
        self._hose = None

    def __enter__(self):
        self._hose = Hose.participate(self._pool_name)
        return self._hose

    def __exit__(self, type, value, traceback):
        self._hose.withdraw()
        if self._created:
            pass
            #TODO: Currently this returns an exception, figure that out!
            #Hose.dispose(self._pool_name)


#load some Proteins
def _read_pro(fname):
    fpath = os.path.join(os.path.dirname(__file__), 'yamlio', fname)
    return yamlio.parse_yaml_protein(open(fpath))
REMOVE_TOPO = _read_pro('remove_topo.protein')


def _deposit_protein(hose, protein):
    p = Protein(descrips=protein.descrips().to_json(), ingests=protein.ingests().to_json())
    hose.deposit(p)
    #TODO: hose.next() should return pyplasma objects
    #ret = hose.next()
    ret = hose.await_next(timeout=1)
    return ret


class TestDS(unittest.TestCase):
    """
    This is more of an integration test than a unittest.
    It is not designed to test that store is working for all the edge cases,
    that should go into insert_test.py.  This is meant to test whether
    messages on the pools go to store/the db without issue.
    """
    def test_remove(self):
        with TempPool(TEST_POOL) as hose:
            pool_pro = _deposit_protein(hose, REMOVE_TOPO)
            self.assertTrue(isinstance(pool_pro, cplasma._pyplasma_api.RProtein))
            exp_descrips = ['sluice', 'prot-spec v1.0', 'topology', 'remove']
            exp_ingests = {'topology': [{'id': 'Electronics'}, {'id': 'Garden Registers'}]}
            #TODO: Do not use to_json method
            self.assertEqual(exp_descrips, pool_pro.descrips().to_json())
            self.assertEqual(exp_ingests, pool_pro.ingests().to_json())


if __name__ == '__main__':
    unittest.main()


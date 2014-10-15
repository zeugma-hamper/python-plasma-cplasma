import unittest
import os.path
import StringIO
from io import BytesIO

#Make sure the test uses the local cplasma instead of the global one
#Do this because this is a library and is very frequently already installed
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


import cplasma
from cplasma import Hose, Protein
from cplasma import yamlio


TEST_POOL = 'temp-datastore-test'
KIND = 'metabo-test-obj'
NOW = -1
ALL = False


IO_FILE = os.path.join(os.path.dirname(__file__), 'yamlio', 'remove_topo.protein')


class TestYamlIO(unittest.TestCase):

    def _check_remove_topo(self, p):
        descrips = p.descrips().to_json()
        ingests = p.ingests().to_json()
        exp_descrips = ['sluice', 'prot-spec v1.0', 'topology', 'remove']
        exp_ingests = {'topology': [{'id': 'Electronics'}, {'id': 'Garden Registers'}]}
        self.assertEqual(exp_descrips, descrips)
        self.assertEqual(exp_ingests, ingests)

    def test_read_file(self):
        p = yamlio.parse_yaml_protein(open(IO_FILE))
        self.assertTrue(isinstance(p, cplasma._pyplasma_api.RProtein))
        self._check_remove_topo(p)

    def test_read_flike(self):
        #TODO: Add a StringIO Test?  They are filelike but do not have a read() method
        #NOTE: I could not inherit from cStringIO.StringIO
        class FileLike(StringIO.StringIO):
            def read(self):
                return self.getvalue()
        p_data = FileLike()
        p_data.write(open(IO_FILE).read())
        #Read from the filelike
        p = yamlio.parse_yaml_protein(p_data)
        self.assertTrue(isinstance(p, cplasma._pyplasma_api.RProtein))
        self._check_remove_topo(p)

if __name__ == '__main__':
    unittest.main()


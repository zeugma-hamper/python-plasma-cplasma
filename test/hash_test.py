import unittest
import os.path

#Make sure the test uses the local cplasma instead of the global one
#Do this because this is a library and is very frequently already installed
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cplasma import Slaw

class NativeTest(unittest.TestCase):
    def test_slaw_hash(self):
        a = Slaw('a')
        b = Slaw('b')
        self.assertNotEqual(hash(a), hash(b))

        d = { a : 'a slaw', b : 'b slaw' }
        
        self.assertEquals('a slaw', d[a])
        self.assertEquals('b slaw', d[b])

    def test_bslaw_hash(self):
        a_ = Slaw('a')
        b_ = Slaw('b')
        a = a_.read()
        b = b_.read()
        self.assertNotEqual(hash(a), hash(b))

        d = { a : 'a slaw', b : 'b slaw' }
        
        self.assertEquals('a slaw', d[a])
        self.assertEquals('b slaw', d[b])


if '__main__' == __name__:
    unittest.main()



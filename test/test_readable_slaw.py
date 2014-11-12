import unittest
import os.path

#Make sure the test uses the local cplasma instead of the global one
#Do this because this is a library and is very frequently already installed
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cplasma import Slaw, Protein

class ReadableSlawTest(unittest.TestCase):
    def testReadIngests(self):
        descrips = Protein(['foo', 'bar'], { 'hello':'world' }).descrips().emit()
        self.assertEqual(['foo', 'bar'], descrips)

        ingests = Protein(['foo', 'bar'], { 'hello':'world'}).ingests().emit()
        self.assertEqual({'hello':'world'}, ingests)

if '__main__' == __name__:
    unittest.main()

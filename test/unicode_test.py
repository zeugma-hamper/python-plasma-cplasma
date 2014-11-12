# -*- coding: UTF-8 -*-
import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cplasma

class TestUnicode(unittest.TestCase):
    def roundTrip(self, s):
        slaw = cplasma.Slaw(s)
        return slaw.read().emit()
        
    def test_english_ascii(self):
        actual = self.roundTrip('hello world')
        self.assertEqual(actual, 'hello world')

    def test_english_unicode(self):
        actual = self.roundTrip(u'hello world')
        self.assertEquals(actual, u'hello world')

    def test_arabic_unicode(self):
        original = u'الدولة_الإسلامية'
        actual = self.roundTrip(original)
        self.assertEquals(actual, original)

if '__main__' == __name__:
    unittest.main()


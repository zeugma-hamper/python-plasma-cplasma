from cplasma_ext import Slaw, SlawBuilder, v3float64
from pprint import pprint
from random import random, randint
import numpy as np

def rndv3():
    return v3float64.make(random(), random(), random())

words = [line.strip() for line in file('/usr/share/dict/words')]

def rndstr():
    return words[randint(0, len(words))]

bu = SlawBuilder ()
for i in range(10):
    bu.mapPut(Slaw.make(rndv3()),
              Slaw.make(rndstr()))
bu.mapPut(Slaw.make("Nada"), Slaw.make(None))
bu.mapPut(Slaw.make("numpy?"), Slaw.make_array(np.array(range(10), np.uint8)))
bu.mapPut(Slaw.make("v3float64_array?"),
          Slaw.make_array(np.array([[1, 2, 3]
                                    for x in range(10)], np.float64)))
l = bu.takeMap()
pprint(l.read().emit())


from cplasma_ext import Slaw, SlawBuilder, v3float64, Hose
from pprint import pprint
from random import random, randint
import numpy as np


h = Hose("py-test-pool")

bu = SlawBuilder()
bu.listAppend (Slaw.make("foo"))
bu.listAppend (Slaw.make("bar"))
bu.listAppend (Slaw.make("baz"))
des = bu.takeList ()

bu.mapPut (Slaw.make("hello"), Slaw.make("world"))
bu.mapPut (Slaw.make("data"), Slaw.make(np.array(range(10), np.uint8)))
ing = bu.takeMap()

pro = Slaw.makeProtein(des, ing)

print(h.deposit(pro))

import signal
import cplasma

from pprint import pprint

mouse = cplasma.Hose("mouse")
try:
    while True:
        tup = mouse.await_next(.5)
        if tup is not None:
            pro, idx, ts = tup
            pprint(pro.ingests.emit())
            pprint(pro.descrips.emit())
except KeyboardInterrupt:
    mouse.wakeup()
        
              

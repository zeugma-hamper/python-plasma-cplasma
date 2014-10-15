"""
Dispatch incoming proteins to entities who may care about them
"""

# (c) 2014 MCT

import cplasma
import cplasma.native

class Metabolizer(object):
    def __init__(self):
        self.__gang = cplasma.native.Gang()
        self.__hoses = []
        self.__metabolizers = []
        self.__quit = False
        self.__busy_time = 0.25

    def quit(self):
        self.__quit = True

    def setBusyWait(self, x):
        self.__busy_time = float(x)

    def poolParticipate(self, hose_name):
        hose = cplasma.native.Hose(hose_name)
        self.__gang.join(hose)
        self.__hoses.append(hose)

    def appendMetabolizer(self, descrips_, fun, name):
        descrips = cplasma.Slaw(descrips_)
        self.__metabolizers.append((descrips, fun, name))

    def removeMetabolizer(self, name):
        self.__metabolizers \
            = [(d, f, n) for (d, f, n) in self.__metabolizers if n != name]

    def metabolizeOne(self):
        bundle = self.__gang.awaitNext(self.__busy_time)
        if bundle:
            bprotein, idx, ts, source = bundle
            for descrips, fun, name in self.__metabolizers:
                if -1 < bprotein.descrips().gapsearch(descrips.read()):
                    fun(bprotein)

    def metabolize(self):
        while not self.__quit:
            self.metabolizeOne()




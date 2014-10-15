import numpy
import cplasma
from cplasma.const import SEARCH_GAP
from collections import OrderedDict

#wrappers around some types
class Wrapped(object):
    def __init__(self, val):
        self._val = val

    def to_json(self, *args):
        #TODO: Support degrade kwargs
        return self._val

class obtimestamp(Wrapped):
    pass

class Index(Wrapped):
    def __int__(self):
        return self._val

class RProtein(object):
    """
    A protein returned from cplasma.native.  This should be treated as a
    read only protein.
    """

    def __init__(self, protein, origin, index, timestamp):
        self.__protein = protein
        self._origin = origin
        self._index = index
        self._timestamp = timestamp

    def __getattr__(self, attr):
        return getattr(self.__protein, attr)

    def to_json(self, *args):
        return _sanitize_for_json(self.__protein.emit())

    def origin(self):
        return self._origin

    def matches(self, needle, how=SEARCH_GAP):
        if how != SEARCH_GAP:
            raise NotImplementedError('Only support the SEARCH_GAP matches currently')
        #need to save as a variable here or else it goes out of scope,
        #and you're reading random garbage from meory
        needle_ = cplasma.Slaw(needle)
        ind = self.__protein.descrips().gapsearch(needle_.read())
        return bool(ind >  -1)

    def descrips(self):
        de = self.__protein.descrips()
        return Descrips(de)

    def ingests(self):
        ing = self.__protein.ingests()
        return Ingests(ing)

    def index(self):
        return Index(self._index)

    def timestamp(self):
        return obtimestamp(self._timestamp)

class Descrips(object):
    def __init__(self, descrips):
        self.__descrips = descrips.emit()

    def __getitem__(self, i):
        return self.__descrips[i]

    def to_json(self, *args):
        return _sanitize_for_json(self.__descrips)

class Ingests(OrderedDict):
    def __init__(self, ingests):
        super(Ingests, self).__init__(ingests.emit())

    def to_json(self, degrade=False):
        return _sanitize_for_json(self)


def _sanitize_for_json(obj):
    """
    Convert to objects that are safe for json, specifically checking for numpy
    arrays, which should be returned as lists.  Also make sure all lists and
    dicts do not have any numpy arrays
    """
    if isinstance(obj, numpy.ndarray) and obj.ndim == 1:
        return obj.tolist()
    elif isinstance(obj, list) or isinstance(obj, tuple):
        clean_list = [None]*len(obj)
        for i in xrange(len(obj)):
            clean_list[i] = _sanitize_for_json(obj[i])
        obj = clean_list
    elif isinstance(obj, dict):
        clean_dict = {}
        for k, v in obj.iteritems():
            clean_dict[k] = _sanitize_for_json(v)
        obj = clean_dict
    return obj


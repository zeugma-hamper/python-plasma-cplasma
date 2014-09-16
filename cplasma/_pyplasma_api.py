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



    ## descrips matching
    def search(self, needle, how=SEARCH_GAP):
        """
        Descrips search.

        This function looks for needle in this protein's descrips, using
        the plasma semantics. That means that the search will only succeed
        if the descrips are an oblist, in which case this functions returns:

        * if needle is a list, self.descrips().search_ex(needle,how)
        * if needle is not a list, self.descrips().search_ex([needle,], how)

        If this protein's descrips are not a list, this function returns a
        negative value. The optional how argument works the same as in the
        oblist method search_ex().
        """
        ## Slaw or bslaw, Protein_Search_Type
        ## return int64
        descrips = self.__protein.descrips
        if type(descrips) != cplasma.native.BSlaw:
            print 'descrips is not a list (%s)' % type(descrips)
            return -1
        if isinstance(needle, cplasma.native.BSlaw):
            pass
        else:
            if isinstance(needle, list):
                if len(needle) == 0:
                    return 0
            else:
                needle = [needle,]
            slneedle = cplasma.Slaw(needle)
        #TODO: Fix this:
        #return descrips.gapsearch(slneedle)

        #TODO: REMOVE THE THE REST OF THIS
        hit = -1
        found = []
        nd_i = 0
        dlist = descrips.emit()
        for i in range(len(dlist)):
            if dlist[i] == needle[nd_i]:
                found.append(True)
                if hit < 0:
                    hit = i
                nd_i += 1
                if nd_i >= len(needle):
                    break
        if len(found) != len(needle):
            return -1
        return hit


    def matches(self, needle, how=SEARCH_GAP):
        """
        Convenience function checking if self.search(needle, how) > -1
        """
        ## Slaw or bslaw, Protein_Search_Type
        ## return obbool
        return bool(self.search(needle, how) > -1)


    def descrips(self):
        de = self.__protein.descrips
        return Descrips(de)

    def ingests(self):
        ing = self.__protein.ingests
        return Ingests(ing)

    def index(self):
        return Index(self._index)

    def timestamp(self):
        return obtimestamp(self._timestamp)

class Descrips(object):
    def __init__(self, descrips):
        self.__descrips = descrips

    def __getitem__(self, i):
        l = self.__descrips.emit()
        return l[i]

    def to_json(self, *args):
        return _sanitize_for_json(self.__descrips.emit())

class Ingests(OrderedDict):
    def __init__(self, ingests):
        _ingests = ingests.emit()
        super(Ingests, self).__init__(_ingests)

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
    elif isinstance(obj, list):
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


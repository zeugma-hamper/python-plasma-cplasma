'''
Compatibility objects to make things a little easier.
'''

# (c) 2014 MCT

import numpy
from cplasma import native
import StringIO
import cStringIO

oblist = list
obbool = bool
unt8 = numpy.uint8
int8 = numpy.int8
unt16 = numpy.uint16
int16 = numpy.int16
unt32 = numpy.uint32
int32 = numpy.int32
unt64 = numpy.uint64
int64 = numpy.int64
float32 = numpy.float32
float64 = numpy.float64
obstring = str
obnumber = numpy.number #parent class for ints & floats

numeric_array=numpy.array

def __chariter(filelike):
    octet = filelike.read(1)
    while octet:
        yield ord(octet)
        octet = filelike.read(1)

def numeric_array_from_file(fp):
    if isinstance(fp, StringIO.StringIO) \
            or isinstance(fp, cStringIO.InputType) \
            or isinstance(fp, cStringIO.OutputType):
        n_arr = numpy.fromiter(__chariter(fp), numpy.uint8)
    else:
        #TODO: Test this
        n_arr = numpy.fromfile(fp)
    return n_arr


# For vector types we have to be a little more careful
# to make sure they're converted in to proper vectors
# as opposed to plain old numeric arrays.

class obmv(object):
    """
    Parent class for vectors.  Pyplasma inherits from obnumber, but that
    does not work here b/c of some compatability issues with numpy's number
    class
    """
    pass

class v2unt8(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.uint8)
    def toSlaw(self):
        return native.Slaw.make_v2unt8(self.data)

class v3unt8(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.uint8)
    def toSlaw(self):
        return native.Slaw.make_v3unt8(self.data)

class v4unt8(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.uint8)
    def toSlaw(self):
        return native.Slaw.make_v4unt8(self.data)

class v2int8(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.int8)
    def toSlaw(self):
        return native.Slaw.make_v2int8(self.data)

class v3int8(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.int8)
    def toSlaw(self):
        return native.Slaw.make_v3int8(self.data)

class v4int8(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.int8)
    def toSlaw(self):
        return native.Slaw.make_v4int8(self.data)

class v2unt16(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.uint16)
    def toSlaw(self):
        return native.Slaw.make_v2unt16(self.data)

class v3unt16(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.uint16)
    def toSlaw(self):
        return native.Slaw.make_v3unt16(self.data)

class v4unt16(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.uint16)
    def toSlaw(self):
        return native.Slaw.make_v4unt16(self.data)

class v2int16(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.int16)
    def toSlaw(self):
        return native.Slaw.make_v2int16(self.data)

class v3int16(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.int16)
    def toSlaw(self):
        return native.Slaw.make_v3int16(self.data)

class v4int16(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.int16)
    def toSlaw(self):
        return native.Slaw.make_v4int16(self.data)

class v2unt32(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.uint32)
    def toSlaw(self):
        return native.Slaw.make_v2unt32(self.data)

class v3unt32(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.uint32)
    def toSlaw(self):
        return native.Slaw.make_v3unt32(self.data)

class v4unt32(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.uint32)
    def toSlaw(self):
        return native.Slaw.make_v4unt32(self.data)

class v2int32(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.int32)
    def toSlaw(self):
        return native.Slaw.make_v2int32(self.data)

class v3int32(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.int32)
    def toSlaw(self):
        return native.Slaw.make_v3int32(self.data)

class v4int32(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.int32)
    def toSlaw(self):
        return native.Slaw.make_v4int32(self.data)

class v2unt64(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.uint64)
    def toSlaw(self):
        return native.Slaw.make_v2unt64(self.data)

class v3unt64(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.uint64)
    def toSlaw(self):
        return native.Slaw.make_v3unt64(self.data)

class v4unt64(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.uint64)
    def toSlaw(self):
        return native.Slaw.make_v4unt64(self.data)

class v2int64(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.int64)
    def toSlaw(self):
        return native.Slaw.make_v2int64(self.data)

class v3int64(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.int64)
    def toSlaw(self):
        return native.Slaw.make_v3int64(self.data)

class v4int64(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.int64)
    def toSlaw(self):
        return native.Slaw.make_v4int64(self.data)

class v2float32(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.float32)
    def toSlaw(self):
        return native.Slaw.make_v2float32(self.data)

class v3float32(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.float32)
    def toSlaw(self):
        return native.Slaw.make_v3float32(self.data)

class v4float32(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.float32)
    def toSlaw(self):
        return native.Slaw.make_v4float32(self.data)

class v2float64(obmv):
    def __init__(self, x, y):
        self.data = numpy.array([x, y], numpy.float64)
    def toSlaw(self):
        return native.Slaw.make_v2float64(self.data)

class v3float64(obmv):
    def __init__(self, x, y, z):
        self.data = numpy.array([x, y, z], numpy.float64)
    def toSlaw(self):
        return native.Slaw.make_v3float64(self.data)

class v4float64(obmv):
    def __init__(self, x, y, z, w):
        self.data = numpy.array([x, y, z, w], numpy.float64)
    def toSlaw(self):
        return native.Slaw.make_v4float64(self.data)


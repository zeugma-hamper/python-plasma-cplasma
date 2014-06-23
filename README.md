
# cplasma

A plasma binding for python.

## Requirements

* `boost::python`
* `numpy`

## Build

Use `distutils`.

## Differences from pyplasma

* `next`/`awaitNext` differences

Calls to `next`/`awaitNext`/etc. on a Hose or HoseGang returns
the following tuple:

    protein, index, timestamp (, pool_name in the case of gangs)

If there is no protein or if a call to await times out, it returns
`None`. pyplasma throws an exception in this case.

* numeric arrays

To send a numeric array as slaw, use `numpy.array`.  Note that
if you want to send a `v3float64` as opposed to an three element
array of `float64` you have to explicitly call `cplasma.native.Slaw.make_v3float64`.

Alternately, in `cplasma.compat` there are classes for all of the
vector types that will do this for you.

* numbers

If you want to send a specific sized and signed numeric type,
you can use the `numpy` dtypes -- `numpy.uint8`, `numpy.float32`,
etc. -- and they will be automatically converted.  Regular integral
types -- `int` and `long` -- are sent as `int64`.  Floating
types are sent as `float64`.


## Use

For now there are a couple of small examples:

* `examples/sluice_heart_watcher.py` shows how to listen to a pool
* `examples/tiled.py` is a small, feature-poor replacemnt for the exiting C++ tiled.

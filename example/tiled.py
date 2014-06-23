'''
A simple, single-threaded map tile fetcher.  For
demonstration purposes only.
'''

# (c) 2014 MCT

from cplasma.metabolizer import Metabolizer
from cplasma import Hose, Protein
import numpy
import os
import os.path
import urllib2

def send_tile(x, y, z, pool, img, map_id):
    p = Protein(['tile-response'],
                { 'x'             : x,
                  'y'             : y,
                  'z'             : z,
                  'map-id'        : map_id,
                  'response-pool' : pool,
                  'bytes'         : img,
                  'image-type'    : 'jpeg' })
    print ('Sending %d,%d,%d to %s' % (x, y, z, pool))
    Hose(pool).deposit(p)

def cache_file(x, y, z):
    cache_root = os.path.join(os.environ['HOME'], 'tmp/cache/mapquest')
    return os.path.join(cache_root, '%d/%d/%d_%d_%d.jpg' % (z, x, z, x, y))

def fetch_cache(x, y, z):
    filename = cache_file(x, y, z)
    if os.path.isfile(filename):
        with file(filename) as fp:
            print('Cache hit for %s' % filename)
            return numpy.fromfile(fp, numpy.uint8)
    else:
        print('Cache miss for %s' % filename)
    return None

def save_cache(x, y, z, arr):
    filename = cache_file(x, y, z)
    if not os.path.isfile(filename):
        # Let's assume that if it's already there, it's good
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with file(filename, 'w') as fp:
            arr.tofile(fp)

def fetch_url(x, y, z):
    url = 'http://otile1.mqcdn.com/tiles/1.0.0/osm/%d/%d/%d.jpg' % (z, x, y)
    print('Fetching %s' % url)
    buf = urllib2.urlopen(url).read()
    return numpy.frombuffer(buf, numpy.uint8)

def fetch_tile(p):
    ing = p.ingests.emit()
    resp_pool, map_id, x, y, z = (ing[k] for k in
                                  ('response-pool', 'map-id', 'x', 'y', 'z'))
    x, y, z = int(x), int(y), int(z)
    blob = fetch_cache(x, y, z)
    if blob is None:
        blob = fetch_url(x, y, z)
        save_cache(x, y, z, blob)
    send_tile(x, y, z, resp_pool, blob, map_id)

def main():
    metabo = Metabolizer()
    metabo.poolParticipate('tiles-req')
    metabo.appendMetabolizer(['tile-request'], fetch_tile, 'fetch-tile')
    metabo.metabolize()

if '__main__' == __name__:
    main()

"""
This is to be a common way to work with Yaml for pyplasma and cplasma.  If you
change this filename or public methods in this file, check pyplasma as well.
"""

import re, cStringIO
import cplasma.native
from cplasma._pyplasma_api import RProtein
from cplasma import Protein

def dump_yaml(obj):
    return '%YAML 1.1\n%TAG ! tag:oblong.com,2009:slaw/\n--- %s' % obj.toYaml()

def dump_yaml_protein(p, fh=None):
    s = p.toYaml()
    if fh is None:
        return s
    else:
        fh.write(s)

def dump_yaml_proteins(ps, fh=None):
    wantoutput = False
    if fh is None:
        wantoutput = True
        fh = cStringIO.StringIO()
    for p in ps:
        fh.write(p.toYaml())
    if wantoutput:
        return fh.getvalue()

def parse_yaml_protein(fh):
    "Return the first protein from a file-ish thing"
    for p in parse_yaml_proteins(fh):
        return p

def parse_yaml_proteins(filelike):
    "Return all proteins from a file-ish thing"
    if hasattr(filelike, 'fileno'):
        fd = filelike.fileno()
        out = [RProtein(Protein(pro.descrips(), pro.ingests()), None, None, None)
               for pro in cplasma.native.Slaw.fromFileDescriptor(fd) if pro.isProtein()]
        return out
    else:
        splitter = re.compile('^\.\.\.$', re.M)
        prots = (x.strip() for x in splitter.split(filelike.read()))
        return [RProtein(cplasma.native.Slaw.fromYaml(pro), None, None, None)
                for pro in prots if 0 < len(pro)]

def parse_yaml_slaw(fh):
    return parse_yaml_proteins(fh)


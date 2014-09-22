"""
This is to be a common way to work with Yaml for pyplasma and cplasma.  If you
change this filename or public methods in this file, check pyplasma as well.
"""
import cplasma.native
from cplasma._pyplasma_api import RProtein

def dump_yaml(obj):
    return '%YAML 1.1\n%TAG ! tag:oblong.com,2009:slaw/\n--- %s' % obj.toYaml()

def dump_yaml_protein(p, fh=None):
    s = p.toYaml()
    if fh is None:
        return s
    else:
        fh.write(s)

def dump_yaml_proteins(ps, fh=None):
    #TODO: Implement this
    raise NotImplementedError

def parse_yaml_protein(fh):
    native_protein = cplasma.native.Slaw.fromYaml(fh.read())
    return RProtein(native_protein, None, None, None)

def parse_yaml_proteins(fh):
    #TODO: Implement this
    raise NotImplementedError

def parse_yaml_slaw(fh):
    return parse_yaml_proteins(fh)


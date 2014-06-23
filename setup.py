from distutils.core import setup
from distutils.extension import Extension
import subprocess, os, os.path, re, numpy

def find_gspeak():
    if 'G_SPEAK_HOME' in os.environ:
        return os.environ['G_SPEAK_HOME']
    g_speak = re.compile('g-speak(\d+\.\d+).*')
    options = []
    for path in os.listdir('/opt/oblong'):
        if os.path.isdir(path):
            m = g_speak.match(path)
            if m:
                options.append((- float(m.group(1)),
                                os.path.join('/opt/oblong', path)))
    if 0 < len(options):
        raise Exception("Could not find a g-speak installation")

    return sorted(options)[0][1]

def cplasma_extension():
    os.environ['G_SPEAK_HOME'] = find_gspeak()
    extra_pkg = os.path.join(os.environ['G_SPEAK_HOME'], 'lib/pkgconfig')
    if 'PKG_CONFIG_PATH' in os.environ:
        os.environ['PKG_CONFIG_PATH'] = ':'.join(os.environ['PKG_CONFIG_PATH'],
                                                 extra_pkg)
    else:
        os.environ['PKG_CONFIG_PATH'] = extra_pkg
        
    compiler_args = subprocess.check_output(['pkg-config', '--cflags', 'libPlasma'])
    linker_args = subprocess.check_output(['pkg-config', '--libs', 'libPlasma'])

    return Extension('cplasma.native',
                     sources = ['cplasma_ext.cpp'],
                     libraries = ['boost_python'],
                     include_dirs = [numpy.get_include()],
                     extra_compile_args = ['-std=c++0x'] + compiler_args.split(),
                     extra_link_args = linker_args.split())


setup(name         = 'cplasma',
      version      = '0.1',
      author       = 'Corey Porter',
      author_email = 'cp@mct.io',
      description  = "native binding to Oblong's plasma library",
      license      = "Entirely proprietary. Don't even think of it",
      keywords     = 'plasma',
      url          = 'http://mct.io/',
      packages     = ['cplasma'],
      ext_modules  = [cplasma_extension()],
      requires     = ['numpy'])

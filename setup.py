from setuptools import setup, Distribution
from setuptools.extension import Extension
import subprocess, os, os.path, re, numpy, platform

OBLONG_DIR = '/opt/oblong'

def find_gspeak():
    if 'G_SPEAK_HOME' in os.environ:
        return os.environ['G_SPEAK_HOME']
    g_speak = re.compile('g-speak(\d+\.\d+).*')
    options = []
    for dirname in os.listdir(OBLONG_DIR):
        path = os.path.join(OBLONG_DIR, dirname)
        if os.path.isdir(path):
            m = g_speak.match(dirname)
            if m:
                options.append((- float(m.group(1)),
                                path))
    if 0 == len(options):
        raise Exception("Could not find a g-speak installation")

    return sorted(options)[0][1]

def cplasma_extension():
    os.environ['G_SPEAK_HOME'] = find_gspeak()
    extra_pkg = os.path.join(os.environ['G_SPEAK_HOME'], 'lib/pkgconfig')
    if 'PKG_CONFIG_PATH' in os.environ:
        os.environ['PKG_CONFIG_PATH'] = ':'.join([os.environ['PKG_CONFIG_PATH'],
                                                  extra_pkg])
    else:
        os.environ['PKG_CONFIG_PATH'] = extra_pkg

    compiler_args = subprocess.check_output(['pkg-config', '--cflags', 'libPlasma']).split()
    linker_args = subprocess.check_output(['pkg-config', '--libs', 'libPlasma'])

    mac = platform.mac_ver()
    if 0 < len(mac[0]):
        compiler_args.append('-DDARWIN')

    return Extension('cplasma.native',
                     sources = ['cplasma_ext.cpp'],
                     libraries = ['boost_python'],
                     include_dirs = [numpy.get_include()],
                     extra_compile_args = ['-std=c++0x'] + compiler_args,
                     extra_link_args = linker_args.split())


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

setup(name         = 'cplasma',
      install_requires = ['numpy'],
      version      = '0.0.3',
      author       = 'MCT',
      author_email = 'suppoert@mct.io',
      description  = "native binding to Oblong's plasma library",
      license      = "Entirely proprietary. Don't even think of it",
      keywords     = 'plasma',
      url          = 'http://mct.io/',
      packages     = ['cplasma'],
      ext_modules  = [cplasma_extension()],
      requires     = ['numpy'],
      distclass    = BinaryDistribution)

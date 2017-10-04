"""
jumany setup
"""
import sys
import os
from distutils.core import setup
from scripts.custom_build import BuildTool

# Don't insert space to be compatible shell script.
MODULE_NAME="jumany" # pylint: disable=C0326
MODULE_VERSION="0.3" # pylint: disable=C0326

_REQUIREMENT = {
    'Python': (3, 3),
    'Windows 64bit': True,
    'Windows 32bit': False,
    'POSIX': True,
}

_SET_UP_ARGS = dict(
    name=MODULE_NAME,
    version=MODULE_VERSION,
    description='Interface for JUMAN Morphological analysis system',
    long_description="""Python interface for
    `JUMAN <http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN>'
    Morphological analysis system.""",
    url='https://github.com/yujakudo/jumany',
    author='yujakudo',
    packages=['jumany'],
    package_dir={'jumany': 'python_module'},
    package_data={'jumany': [
        'COPYING', 'README.md', '*.txt', '*.so', 'jumanrc',
        'dics/*/*.pat', 'dics/*/*.mat', 'dics/*/*.dat', 'dics/*/*.tab',
        'dics/*/JUMAN.*'
    ]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Text Processing",
    ],
)

_BUILD_INFO_DICT = {
    'Windows 64bit': {
        'test_dir': "test",
    },
    'POSIX': {
        'tools': ['tar', 'patch', 'make'],
        'scripts': {
            'build': ["scripts/build_ext.sh build"],
            'clean': ["scripts/build_ext.sh clean"],
        },
        'targets': ["build/lib/jumany/libjuman.so"],
        'test_dir': "test",
    }
}

# General process

# Get system
_SYSTEM = None
if os.name == 'nt':
    if sys.maxsize <= 2**32:
        _SYSTEM = 'Windows 32bit'
    else:
        _SYSTEM = 'Windows 64bit'
elif os.name == 'posix':
    _SYSTEM = 'POSIX'

# Get package name and directory
_PACKAGE_NAME = _SET_UP_ARGS['packages'][0]
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DIR = os.path.join(_BASE_DIR, _PACKAGE_NAME)
if 'package_dir' in _SET_UP_ARGS and _PACKAGE_NAME in _SET_UP_ARGS['package_dir']:
    _PACKAGE_DIR = os.path.join(
        _BASE_DIR, _SET_UP_ARGS['package_dir'][_PACKAGE_NAME]
    )

# Set long description from README.txt
# _README = os.path.join(_PACKAGE_DIR, 'README.txt')
# if os.path.exists(_README):
#     with open(_README, 'rb') as fp:
#         _SET_UP_ARGS['long_description'] = fp.read().decode('utf8')

# Set custom build info.
_BUILD_INFO = None
if _SYSTEM in _BUILD_INFO_DICT:
    BuildTool.set_def_options(**_BUILD_INFO_DICT[_SYSTEM])
    BuildTool.set_def_options(cwd=_BASE_DIR)
    BuildTool.update_setup_arg(_SET_UP_ARGS)

# Check system requirement.
if "install" in sys.argv:
    msg = ""
    if not _SYSTEM in _REQUIREMENT or _REQUIREMENT[_SYSTEM] is False:
        msg += "%s can not be installed on %s system.\n" % (_PACKAGE_NAME, _SYSTEM)
    if sys.version_info < _REQUIREMENT['Python']:
        msg += "Python %d.%d or above is required.\n" % _REQUIREMENT['Python']
    if msg != "":
        sys.stderr.write(msg)
        sys.exit(-1)

# Setup
setup(**_SET_UP_ARGS)

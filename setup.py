"""
jumany setup
"""
from distutils.core import setup
import sys
import os
import codecs

_REQ_PYTHON_VER = (3, 3)

_SET_UP_ARGS = dict(
    name='jumany',
    version='0.2',
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
    scripts=['scripts/jumany-i.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved",
        "Operating System :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Text Processing",
    ],
)

if os.path.exists('python_module/README.txt'):
    _SET_UP_ARGS['long_description'] = codecs.open(
        'python_module/README.txt', 'r', 'utf-8').read()

if "install" in sys.argv:
    if sys.platform != "win32" or sys.maxsize <= 2**32:
        print("This module can be installed on Windows 64 bit systems only.")
        sys.exit(-1)
    if sys.version_info < _REQ_PYTHON_VER:
        print("Python v{0}.{1} or above is required.".format(
            _REQ_PYTHON_VER[0], _REQ_PYTHON_VER[1]
        ))
        sys.exit(-1)

setup(**_SET_UP_ARGS)

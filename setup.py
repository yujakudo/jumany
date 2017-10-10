"""
jumany setup
"""
from scripts.setup_ext import SetupExt

# Don't insert space to be compatible shell script.
MODULE_NAME="jumany" # pylint: disable=C0326
MODULE_VERSION="0.4.5" # pylint: disable=C0326

DEVELOPMENT_STATE = 4   # Beta
PACKAGE = MODULE_NAME

_EXT = SetupExt(
    name=MODULE_NAME,
    version=MODULE_VERSION,
    description='Interface for JUMAN Morphological analysis system',
    packages=[PACKAGE, PACKAGE+'.test'],
    package_dir={
        PACKAGE: 'python_module',
        PACKAGE+'.test': 'python_module/test'
    },
    package_data={PACKAGE: ['README.*', '*.txt']},
    license='BSD+LGPL',
    author='yujakudo',
    url='https://github.com/yujakudo/jumany',
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
)

_EXT.set_requirement(
    python=[(3, 3)],
    win64=True,
    win32=True,
    posix=True,
)

_EXT.set_extensions(
    posix={
        'libjuman': dict(
            description='library of JUMAN',
            src_dir='juman-7.01/lib',
            define_macros=[('HAVE_CONFIG_H', 1)],
            include_dirs=['juman-7.01/lib', 'scripts'],
            extra_compile_args=["-Wno-error=format-security", "-O3", "-march=native"],
        )
    }
)

_EXT.set_custom_build(
    for_all=[
        'copy scripts/jumanrc.win jumanrc',
        'copy_tree dist/juman-7.01_ext_win64/dics dics'
    ],
    win64=[
        'copy dist/juman-7.01_ext_win64/lib/libjuman.so libjuman.win64.so',
        'copy copyings/copying.libjuman.win.txt LICENSE.libjuman.txt',
    ],
    win32=[
        'copy dist/juman-7.01_ext_win32/lib/libjuman.so libjuman.win32.so',
        'copy copyings/copying.libjuman.win.txt LICENSE.libjuman.txt',
    ],
    posix=[
        'copy copyings/copying.libjuman.txt LICENSE.libjuman.txt',
    ],
)

_EXT.set_development_state(DEVELOPMENT_STATE)
_EXT.set_crypted_mailaddr('bffq.lhwnxhqb@pbz')

_EXT.setup()

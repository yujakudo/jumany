"""
setup extention
"""
import os
import sys
import glob
import shlex
import inspect
import pprint
from distutils.command.build import build
import setuptools

_SYSTEMS = {
    'posix': 'POSIX',
    'win32': 'Windows 32bit',
    'win64': 'Windows 64bit',
}

_SYSTEM_CLASSFIERS = {
    'posix': "Operating System :: POSIX",
    'win32': "Operating System :: Microsoft :: Windows",
    'win64': "Operating System :: Microsoft :: Windows",
}

_DEV_STATUS_CLASSFIERS = [
    '',
    "Development Status :: 1 - Planning",
    "Development Status :: 2 - Pre-Alpha",
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Development Status :: 6 - Mature",
    "Development Status :: 7 - Inactive",
]

_LICESE_CLASSFIERS = {
    'MIT': "License :: OSI Approved :: MIT License",
    'BSD': "License :: OSI Approved :: BSD License",
    'Apache': "License :: OSI Approved :: Apache Software License",
    'Apache 2.0': "License :: OSI Approved :: Apache Software License",
    'LGPL': "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
}

_PY_MAX_MINORS = [0, 0, 7, 6, 0]

class SetupExt: # pylint: disable=R0902
    """ Setup extention """

    def __init__(self, **setup_args):
        """ condtructor
        @param setup_args arguments of setup to extent
        """
        self.args = setup_args
        self.system_req = None
        self.python_req_min = [None for x in _PY_MAX_MINORS]
        self.caller = inspect.currentframe().f_back.f_code.co_filename
        self.base_dir = os.path.dirname(self.caller)
        # Get system
        self.system = None
        if os.name == 'nt':
            if sys.maxsize <= 2**32:
                self.system = 'win32'
            else:
                self.system = 'win64'
        elif os.name == 'posix':
            self.system = 'posix'
        # Get package name and directory
        self.package_name = self.args['packages'][0]
        self.package_dir = os.path.join(self.base_dir, self.package_name)
        if 'package_dir' in self.args and self.package_name in self.args['package_dir']:
            self.package_dir = os.path.join(
                self.base_dir, self.args['package_dir'][self.package_name]
            )
        # Set long descrition
        if 'long_description' not in self.args:
            self.args['long_description'] = self.args['description']
            fn = None
            for ext in ['', '.rst', '.txt']:
                fn = os.path.join(self.package_dir, 'README'+ext)
                if os.path.exists(fn):
                    with open(fn, 'rb') as fp:
                        self.args['long_description'] = fp.read().decode('utf8').replace("\r\n", '\n')
                    break
        # Set classifiers of licenses
        if 'classifiers' not in self.args:
            self.args['classifiers'] = []
        if 'license' in self.args:
            for license in self.args['license'].split('+'):
                if license in _LICESE_CLASSFIERS:
                    self.args['classifiers'].append(_LICESE_CLASSFIERS[license])

    def set_development_state(self, code: int):
        """ Set development state
        @param code development state from 1 to 6.(3 to 5 are common)
        """
        self.args['classifiers'].append(_DEV_STATUS_CLASSFIERS[code])

    def set_requirement(self, **req):
        """ Set system requirement
        @param python List of taple of minimum version to allow.
        e.g.[(2,5), (3,3)]
        @param posix, win32, win64 Not False if supported
        """
        self.system_req = req
        if 'platforms' not in self.args:
            self.args['platforms'] = []
        for sys_name in _SYSTEMS:
            if sys_name in self.system_req and self.system_req[sys_name] is not False:
                classfier = _SYSTEM_CLASSFIERS[sys_name]
                if classfier not in self.args['classifiers']:
                    self.args['classifiers'].append(classfier)
                    splited = classfier.split(' ')
                    self.args['platforms'].append(splited[-1])                    
        if 'python' in self.system_req:
            max_major = 0
            pyreq = ''
            for ver in self.system_req['python']:
                self.python_req_min[ver[0]] = ver[1]
                pyreq += ', ' if pyreq != '' else ''
                pyreq += ">=%d.%d" % (ver[0], ver[1])
                max_major = ver[0] if ver[0] > max_major else max_major
                max_minor = _PY_MAX_MINORS[ver[0]]
                for minor in range(ver[1], max_minor + 1):
                    self.args['classifiers'].append(
                        "Programming Language :: Python :: %d.%d" % (ver[0], minor)
                    )
            if max_major > 0:
                if 'python_requires' not in self.args:
                    self.args['python_requires'] = pyreq + ", <%d" % (max_major + 1)

    def set_extensions(self, **exts):
        """ Set info. to build extension libraries
        Each parameter takes a dict of extension.
        Value is saame as setuptools.Extension(), but added parameters.
        - description: Short description for error or help.
        - src_dir: Source directory to extract to 'sources'
        @param posix, win32, win64
        """
        if self.system not in exts:
            return
        features = {}
        for name, ext_args in exts[self.system].items():
            if not 'name' in ext_args:
                ext_args['name'] = self.package_name + '.' + name
            if 'src_dir' in ext_args:
                ext_args['sources'] = glob.glob(ext_args['src_dir'] + '/*.c*')
                del ext_args['src_dir']
            desc = ext_args['name']
            if 'description' in ext_args:
                desc = ext_args['description']
                del ext_args['description']
            features[name] = setuptools.Feature(
                desc, standard=True,
                ext_modules=[setuptools.Extension(**ext_args)]
            )
        self.args['features'] = features

    def set_custom_build(self, for_all=None, **custom):
        """ Custom build
        Each parameter is a List of commandline.
        Parameter dest is relative path from package directory.
        Commands are follows:
        - copy: 'copy src dest': Copy file src to dest.
        - copy_tree: 'copy_tree src dest': Copy directory src to dest.
        - move: 'move src dest': Move file src to dest.
        - mkpath: 'mkpath dest mode': Make directory dest. default of mode is '0o777'
        - execute: 'execute func args...': ececute function
        - spawn: 'spawn cmd': execute cmd in subprocess.
        @param for_all, posix, win64, win32
        """
        CustomBuild.set_pakage_name(self.package_name)
        if isinstance(for_all, list):
            CustomBuild.set_rules(for_all)
        if self.system in custom:
            CustomBuild.set_rules(custom[self.system])
        if CustomBuild.count_rules() == 0:
            return
        if 'cmdclass' not in self.args:
            self.args['cmdclass'] = {}
        self.args['cmdclass']['build'] = CustomBuild

    def get_args(self)->dict:
        """ Get setup arguments """
        return self.args

    def _show(self):
        """ Show arguments and exit when 'show' entered """
        if "show" not in sys.argv:
            return
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.args)
        sys.exit(0)

    def _check_requirement(self):
        """ Check requirement when install
        Exit if this system not supported.
        """
        if "install" not in sys.argv:
            return
        msg = ""
        if not self.system in self.system_req or self.system_req[self.system] is False:
            msg += "%s system is not supported.\n" % _SYSTEMS[self.system]
        ver = sys.version_info
        min_minor = self.python_req_min[ver[0]]
        if min_minor is None or ver[1] < min_minor:
            msg += "Python %d.%d is not supported.\n" % (ver[0], ver[1])
            msg += "Followings are required.\n"
            for majour, min_minor in enumerate(self.python_req_min):
                if majour:
                    msg += "- Python %d.%d or above.\n" % (majour, min_minor)
        if msg != "":
            sys.stderr.write(
                "%s can not be installed on this system.\n" % self.package_name
            )
            sys.stderr.write(msg)
            sys.exit(-1)

    def setup(self):
        """ Do setup """
        self._show()
        self._check_requirement()
        setuptools.setup(**self.args)

    @staticmethod
    def _crypt_addr(addr: str)->str:
        crypted = ''
        for c in addr:
            asc = ord(c)
            if 'a' <= c and c <= 'z': # pylint: disable=C0122
                asc += 13 if c < 'n' else -13
            if 'A' <= c and c <= 'Z': # pylint: disable=C0122
                asc += 13 if c < 'N' else -13
            if '0' <= c and c <= '9': # pylint: disable=C0122
                asc += 5 if c < '5' else -5
            if c == '@':
                asc = ord('.')
            if c == '.':
                asc = ord('@')
            crypted += chr(asc)
        return crypted

    def set_crypted_mailaddr(self, addr: str)->str:
        """ Set crypted mail address """
        self.args['author_email'] = self._crypt_addr(addr)

class CustomBuild(build):
    """ Overwrite build """
    _rules = []
    _package_name = None
    @staticmethod
    def set_pakage_name(name: list):
        """ set package name """
        CustomBuild._package_name = name
    @staticmethod
    def set_rules(rules: list):
        """ set rule """
        CustomBuild._rules += rules
    @staticmethod
    def count_rules():
        """ Get number of rules """
        return len(CustomBuild._rules)

    def path_from_package(self, path: str)->str:
        """ get path from package directory """
        return os.path.join(self.build_lib, CustomBuild._package_name, path)

    def run(self):
        """ run build process """
        build.run(self)
        for rule in CustomBuild._rules:
            args = shlex.split(rule)
            cmd = args.pop(0)
            if cmd == 'copy':
                args[1] = self.path_from_package(args[1])
                self.copy_file(*args)
            elif cmd == 'copy_tree':
                args[1] = self.path_from_package(args[1])
                self.copy_tree(*args)
            elif cmd == 'move':
                args[1] = self.path_from_package(args[1])
                self.move_file(*args)
            elif cmd == 'mkpath':
                args[0] = self.path_from_package(args[0])
                self.mkpath(*args)
            elif cmd == 'execute':
                func = args.pop(0)
                self.execute(func, args)
            elif cmd == 'spawn':
                self.spawn(*args)

if __name__ == '__main__':
    _EXT = SetupExt(
        name="test_module",
        version="0.1",
        description='Test module',
        packages=['jumany'],
        package_dir={'jumany': 'python_module'},
    )

    _EXT.set_requirement(
        python=[(2, 5), (3, 3)],
        win64=True,
        win32=True,
        posix=True,
    )
    _EXT.set_development_state(4)
    _EXT.set_extensions(
        win64={
            'libjuman': dict(
                description='library of JUMAN',
                src_dir='juman-7.01/lib',
            )
        }
    )
    _EXT.set_custom_build(
        win64=[
            'copy dist/juman-7.01_ext_win64/lib/libjuman.so libjuman.win64.so',
        ],
    )
    sys.argv = ["hoge", "install"]
    print(repr(_EXT.get_args()))

"""
Custom Build Ext
"""
import os
import sys
import copy
import locale
import shlex
import subprocess
# for custom commands
from distutils.errors import DistutilsError
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.core import Command
# for tests
from unittest import TestLoader
from unittest import TextTestRunner

class BuildTool:
    """	Tool for custom build """

    _def_options = {
        "shell": None,
        "cwd": os.path.join(os.path.dirname(__file__), ".."),
        "tools": {},
        "scripts": {},
        "targets": [],
        "test_dir": None,
    }

    @staticmethod
    def set_def_options(**options):
        """ Set default options """
        BuildTool._def_options.update(options)

    @staticmethod
    def update_setup_arg(args):
        """ Update setup argument to add custom commands """
        args['cmdclass'] = {}
        if 'build' in BuildTool._def_options['scripts']:
            args['cmdclass']['build'] = CustomBuild
        if 'clean' in BuildTool._def_options['scripts']:
            args['cmdclass']['clean'] = CustomClean
        if BuildTool._def_options['test_dir'] is not None:
            args['cmdclass']['test'] = CustomTest

    def __init__(self, **options):
        """ Constractor
        @param cwd Working directory
        @param shell List of shell commandline e.g. ["bash", "-c"]. Default is None.
        @param tools List of command to use in scripts.
        @param scripts Dict. of script. A script is list of commandlines
        @param targets List of path of built. if relative, it from cwd
        @param test_dir String of tests directory.
        """
        self.options = copy.deepcopy(BuildTool._def_options)
        self.options.update(options)
        self.cwd = self.options['cwd']
        self.log = ''
        self.log_path = os.path.join(self.cwd, 'custom_build.log')
        self.encoding = locale.getpreferredencoding()

    def _echo(self, msg: str, echo: bool = True):
        """ Echo and Log """
        if echo:
            print(msg)
        self.log += msg + "\n"

    def _fail_to(self, obj: str, excep: Exception = None):
        """ Echoo 'fail to ...' """
        self._echo("Fail to %s." % obj)
        if excep is not None:
            self._echo("exception: %s" % repr(excep.args), False)
        return False

    def _resolve_path(self, path: str)->str:
        """ Resolve if relative path """
        if path[0] != '/'and path[1] != "\\" and path[1] != ':':
            path = os.path.join(self.cwd, path)
        return path

    def check_tools(self)->bool:
        """ Chec tools for building """
        self._echo("- Checking tools ...")
        res = True
        for tool in self.options['tools']:
            cmd = tool + " --version"
            if self._exec_cmd(cmd):
                self._echo("OK: " + tool)
            else:
                self._echo("NG: " + tool)
                res = False
        if not res:
            self._echo("Some tools for building don't exist.")
        return res

    def exec_script(self, name)->bool:
        """ Execute script """
        self._echo("- Executing %s ..." % name)
        if not name in self.options['scripts']:
            self._echo("Wrong script name: %s" % name)
            return False
        for command_line in self.options['scripts'][name]:
            if not self._exec_cmd(command_line):
                return False
        return True

    def _exec_cmd(self, command_line: str)->bool:
        """ Execute command line """
        keys = {'cwd': self.cwd}
        if self.options['shell'] is None:
            keys['shell'] = True
        else:
            command_line = self.options['shell'] % command_line
        self._echo("> " + command_line)
        cmd = shlex.split(command_line)
        self._echo("splited commandline: " + repr(cmd), False)
        try:
            res = subprocess.check_output(cmd, **keys)
            self._echo(res.decode(self.encoding), False)
        except subprocess.CalledProcessError as e:
            self._echo(e.output.decode(self.encoding), False)
            return self._fail_to("execute", e)
        except Exception as e: # pylint: disable=W0703
            return self._fail_to("execute", e)
        return True

    def check_targets(self)->bool:
        """ Check all target exists """
        self._echo("- Checking targets have been built ...")
        res = True
        for target in self.options['targets']:
            path = self._resolve_path(target)
            if os.path.exists(path):
                self._echo("OK: %s" % path)
            else:
                res = False
                self._echo("NG: %s" % path)
        return res

    def exec_all(self, script_name)->bool:
        """Execute all"""
        res = False
        if 'clean' in self.options["scripts"]:
            self.exec_script('clean')
        if self.check_tools() and self.exec_script(script_name) and self.check_targets():
            res = True
        else:
            print("For more information, see log: %s" % self.log_path)
        with open(self.log_path, 'w') as fl:
            fl.write(self.log)
        self.log = ''
        return res

    def test(self)->bool:
        """ Execute tests """
        if self.options['test_dir'] is None:
            print("Nothing to do.")
            return
        path = self._resolve_path(self.options['test_dir'])
        print(path)
        tests = TestLoader().discover(path)
        TextTestRunner().run(tests)

class CustomBuild(build):
    """ Overwrite build """
    def run(self):
        """ run build process """
        if not BuildTool().exec_all('build'):
            raise DistutilsError('Fail to custom build.')
        build.run(self)

class CustomClean(clean):
    """ Overwrite clean """
    def run(self):
        """ Run clean process """
        BuildTool().exec_script('clean')
        clean.run(self)

class CustomTest(Command):
    """ Exec tests """
    description = "Execute tests"

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        """ Run test process """
        BuildTool().test()

# Test
if __name__ == '__main__':
    _INFO_DICT = {
        'nt': {
            'cwd': os.path.join(os.path.dirname(__file__), "../test/custom_build"),
            'scripts': {
                'build': ["build.bat build"],
                'clean': ["build.bat clean"],
            },
            'targets': ['made.so'],
        },
        'posix': {
            'cwd': os.path.join(os.path.dirname(__file__), "../test/custom_build"),
            'scripts': {
                'build': ["build.sh build"],
                'clean': ["build.sh clean"],
            },
            'targets': ['made.so'],
        },
    }
    _INFO = _INFO_DICT[os.name]
    BuildTool.set_def_options(**_INFO)
    _TOOL = BuildTool()
    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        _TOOL.exec_script('clean')
    else:
        _TOOL.exec_all('build')

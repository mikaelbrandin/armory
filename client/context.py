__author__ = 'kra869'

import argparse
import os
import os.path
import ConfigParser

import modules as mods


class ReadWriteDirectory(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentError(self, "readable_dir:{0} is not a valid path".format(prospective_dir))

        if not os.access(prospective_dir, os.R_OK):
            raise argparse.ArgumentError(self, "readable_dir:{0} is not a readable directory".format(prospective_dir))

        if os.access(prospective_dir, os.W_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentError(self, "writable_dir:{0} is not a writable directory".format(prospective_dir))


def is_armory_repository_dir(dir):
    if not dir.endswith(os.sep):
        dir += os.sep

    if not os.path.isdir(dir):
        return False
    elif not os.access(dir, os.R_OK):
        return False
    elif not os.path.exists(dir + '.armory' + os.sep):
        return False
    elif not os.access(dir, os.W_OK):
        return False

    return True


def root_path():
    return os.path.abspath(os.sep)


class Context:
    def __init__(self):
        self.modules = mods.Modules()
        self.home_directory = os.getcwd() + os.sep

        if not self.home_directory.endswith(os.sep):
            self.home_directory += os.sep

        self.db_directory = self.home_directory + '.armory' + os.sep
        self.branch_file = None

        self.branch = ConfigParser.SafeConfigParser()
        self.config = ConfigParser.SafeConfigParser()
        self.user = ConfigParser.SafeConfigParser()

        self.user_directory = os.path.expanduser('~' + os.getlogin()) + os.sep
        if os.path.exists(self.user_directory + '.armory'):
            self.user.read(self.user_directory + '.armory')

        self.environment = 'dev'
        self.env = {
            'ARMORY_ENV': self.environment,
            'ARMORY_VERSION': '1.0.0'
        }

        self.args_parser = argparse.ArgumentParser(prog='Armory')
        self.args_parser.add_argument('--debug', action='store_true', help='Enable debugging (mainly)')
        self.args_parser.add_argument('--environment', metavar='ENV', help='use ENV as current environment')
        self.args_parser.add_argument('--directory', metavar='DIRECTORY', default=os.getcwd() + os.sep)
        self.sub_args_parsers = self.args_parser.add_subparsers(title='Armory commands', description='The commands available with Armory', help='Available Armory commmands')

    def register_command(self, cmd, command, **kwargs):
        if kwargs.get('help') is None:
            kwargs['help'] = '<No Help Available>'

        parser = self.sub_args_parsers.add_parser(cmd, help=kwargs.get('help'))
        parser.set_defaults(command=command, directory_filter=kwargs.get('directory_filter'))

        return parser

    def execute(self):
        _args = self.args_parser.parse_args()

        if _args.directory_filter:
            _args.directory = _args.directory_filter(_args);

        if not _args.directory.endswith(os.sep):
            _args.directory += os.sep

        self.home_directory = self.resolve_home_dir(_args.directory)
        self.db_directory = _args.directory + '.armory' + os.sep

        self.config.read(self.db_directory + 'config')

        if _args.environment is not None:
            self.environment = _args.environment
        elif self.config.has_option('environment', 'default'):
            self.environment = self.config.get('environment', 'default')

        self.branch_file = self.home_directory + self.environment + '.armory'
        self.branch.read(self.branch_file)

        if self.branch.has_section('environment'):
            for (key, value) in self.branch.items('environment'):
                self.env['ARMORY_' + key.upper()] = value

        self.env['ARMORY_HOME'] = self.home_directory

        _args.command(_args, self)
        return None

    def resolve_home_dir(self, directory):
        _dir = directory
        _root = root_path()

        while not is_armory_repository_dir(_dir) and not _dir == _root:
            _dir = os.path.dirname(_dir)

        if not is_armory_repository_dir(directory):
            # FIXME: Should be changed to 'user' rather than 'profile'
            if self.user.has_option('profile', 'home') and is_armory_repository_dir(self.user.get('profile', 'home')):
                _dir = self.user.get('profile', 'home')
            elif 'ARMORY_HOME' in os.environ and is_armory_repository_dir(os.environ.get('ARMORY_HOME')):
                _dir = os.environ.get('ARMORY_HOME')

        if not _dir.endswith(os.sep):
            _dir += os.sep
        return _dir

    def check_directories(self):
        pass

    def get_module_directory(self, module_name, version):
        return self.home_directory + 'modules.d' + os.sep + module_name + os.sep + version + os.sep

    def get_modules_directory(self):
        return self.home_directory + 'modules.d' + os.sep

    def get_config_directory(self, module_name, env_name):
        return self.home_directory + 'conf.d' + os.sep + module_name + os.sep + env_name + os.sep


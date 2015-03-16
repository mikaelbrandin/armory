__author__ = 'kra869'

import argparse
import os
import os.path
import glob
import ConfigParser

import utils


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
    elif not os.path.exists(dir + '.armory'):
        return False
    elif not os.access(dir, os.W_OK):
        return False

    return True


class ReadWriteRepositoryDirectory(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not prospective_dir.endswith(os.sep):
            prospective_dir += os.sep

        if is_armory_repository_dir(prospective_dir):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentError(self, "ReadWriteRepositoryDirectory:{0} is not a armoery directory directory".format(prospective_dir))


class Context:
    def __init__(self):
        self.modules = Modules()
        self.home_directory = os.getcwd() + os.sep

        self.initialize_global_configuration()

        if not self.home_directory.endswith(os.sep):
            self.home_directory += os.sep

        self.db_directory = self.home_directory + '.armory' + os.sep
        self.config = ConfigParser.SafeConfigParser()
        self.environment = 'dev'
        self.env = {
            'ARMORY_ENV': self.environment,
            'ARMORY_VERSION': '1.0.0'
        }

        self.args_parser = argparse.ArgumentParser(prog='Armory')
        self.args_parser.add_argument('--debug', action='store_true', help='Enable debugging (mainly)')
        self.args_parser.add_argument('--directory', metavar='FILE', action=ReadWriteRepositoryDirectory, default=self.home_directory)
        self.sub_args_parsers = self.args_parser.add_subparsers(title='Armory commands', description='The commands available with Armory', help='Available Armory commmands')

    def register_command(self, cmd, command, **kwargs):
        if kwargs.get('help') is None:
            kwargs['help'] = '<No Help Available>'

        parser = self.sub_args_parsers.add_parser(cmd, help=kwargs.get('help'))
        parser.set_defaults(command=command)

        return parser

    def initialize_global_configuration(self):
        conf = ConfigParser.SafeConfigParser()
        
        home_dir = os.path.expanduser("~")
        
        if os.path.exists(home_dir+'/.armory'):
            conf.read(home_dir+'/.armory')
            
        if not is_armory_repository_dir(self.home_directory):
            if conf.has_option('profile', 'home') and is_armory_repository_dir(conf.get('profile', 'home')):
                
                dir = conf.get('profile', 'home')
                if not dir.endswith(os.sep):
                    dir += os.sep
                    
                self.home_directory = dir
            elif 'ARMORY_HOME' in os.environ and is_armory_repository_dir(os.environ.get('ARMORY_HOME')):
                self.home_directory = os.environ.get('ARMORY_HOME')

        return conf

    def execute(self):
        args = self.args_parser.parse_args()

        self.home_directory = args.directory
        self.db_directory = args.directory + '.armory' + os.sep

        self.config.read(glob.glob(self.home_directory + '*.armory'))

        if self.config.has_section('environment'):
            for (key, value) in self.config.items('environment'):
                if key == 'env' or key == 'environment':
                    self.env['ARMORY_ENV'] = value
                else:
                    self.env['ARMORY_' + key.upper()] = value

        self.env['ARMORY_HOME'] = args.directory

        args.command(args, self)

        return None

    def check_directories(self):
        pass

    def get_module_directory(self, module_name):
        return self.home_directory + 'modules.d' + os.sep + module_name + '/'

    def get_modules_directory(self):
        return self.home_directory + 'modules.d' + os.sep

    def get_config_directory(self, module_name, env_name):
        return self.home_directory + 'conf.d' + os.sep + module_name + os.sep + env_name + os.sep


class Module:
    MAX_SHORT_DESC_LENGTH = 50

    def __init__(self, module_directory, context):

        if not os.path.isdir(module_directory):
            raise NotImplementedError()

        self.context = context

        self.module_directory = module_directory
        self.name = os.path.basename(module_directory[:-1])

        self.friendly_name = self.name
        self.module_info_file = self.module_directory + self.name + '.info'

        self.version = '~'
        self.description = ''
        self.short_description = ''
        self.config = ConfigParser.SafeConfigParser()
        self.sync()

    def __conf_get(self, name, val):
        if self.config.has_option('general', name):
            return self.config.get('general', name)
        else:
            return val


    def get_processes(self):

        if os.path.exists(self.context.db_directory + 'run/' + self.name + '.pid'):
            return [open(self.context.db_directory + 'run/' + self.name + '.pid', 'r').read()]
        elif os.path.exists(self.module_directory + 'ps'):
            return [int(x) for x in utils.cmd(self.module_directory + 'ps').splitlines()]
        else:
            return []

    def sync(self):
        if not os.path.exists(self.module_info_file):
            return False

        self.config.read(self.module_info_file)

        self.version = self.__conf_get('version', self.version)
        self.friendly_name = self.__conf_get('name', self.name)

        if self.config.has_option('general', 'description'):
            self.description = self.config.get('general', 'description')
            self.short_description = self.description.strip().replace('\n', ' ')
            self.short_description = self.short_description.replace('\t', ' ')
            if len(self.short_description) > Module.MAX_SHORT_DESC_LENGTH:
                self.short_description = self.short_description[0:Module.MAX_SHORT_DESC_LENGTH - 3] + '...'

        return True


class Modules:
    def __init__(self):
        pass


    def get(self, context, module_name):
        return Module(context.get_module_directory(module_name), context)

    def from_context(self, context):
        modules = {}
        
        try:
            for subdirectory in os.listdir(context.get_modules_directory()):
                modules[subdirectory] = self.get(context, subdirectory)
        except:
            return modules

        return modules

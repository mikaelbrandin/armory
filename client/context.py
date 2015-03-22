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
    elif not os.path.exists(dir + '.armory' + os.sep):
        return False
    elif not os.access(dir, os.W_OK):
        return False

    return True
    
def root_path():
    os.path.abspath(os.sep)

class Context:
    def __init__(self):
        self.modules = Modules()
        self.home_directory = os.getcwd() + os.sep

        if not self.home_directory.endswith(os.sep):
            self.home_directory += os.sep

        self.db_directory = self.home_directory + '.armory' + os.sep
        
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
        self.args_parser.add_argument('--directory', metavar='DIRECTORY', default=os.getcwd()+os.sep)
        self.sub_args_parsers = self.args_parser.add_subparsers(title='Armory commands', description='The commands available with Armory', help='Available Armory commmands')

    def register_command(self, cmd, command, **kwargs):
        if kwargs.get('help') is None:
            kwargs['help'] = '<No Help Available>'

        parser = self.sub_args_parsers.add_parser(cmd, help=kwargs.get('help'))
        parser.set_defaults(command=command, directory_filter=kwargs.get('directory_filter'))

        return parser
        
    def execute(self):
        args = self.args_parser.parse_args()

        if args.directory_filter:
            args.directory = args.directory_filter(args);

        if not args.directory.endswith(os.sep):
            args.directory += os.sep

        self.home_directory = self.resolve_home_dir(args.directory)
        self.db_directory = args.directory + '.armory' + os.sep
        
        self.config.read(self.db_directory+'config')
        
        if not args.environment is None:
            self.environment = args.environment
        elif self.config.has_option('environment', 'default'):
            self.environment = self.config.get('environment', 'default')
            
        self.branch_file = self.home_directory + self.environment+'.armory'
        self.branch.read(self.branch_file)

        if self.branch.has_section('environment'):
            for (key, value) in self.branch.items('environment'):
                self.env['ARMORY_' + key.upper()] = value

        self.env['ARMORY_HOME'] = self.home_directory

        args.command(args, self)
        return None
        
    def resolve_home_dir(self, directory):
        dir = directory
        root = root_path()
        
        while not is_armory_repository_dir(dir) and not dir == root:
            dir = os.path.dirname(dir)
        
        if not is_armory_repository_dir(directory):
            #FIXME: Should be changed to 'user' rather than 'profile'
            if self.user.has_option('profile', 'home') and is_armory_repository_dir(self.user.get('profile', 'home')):
                dir = self.user.get('profile', 'home')
            elif 'ARMORY_HOME' in os.environ and is_armory_repository_dir(os.environ.get('ARMORY_HOME')):
                dir = os.environ.get('ARMORY_HOME')
    
        if not dir.endswith(os.sep):
                    dir += os.sep
        return dir

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
        self.status = "ok"

        if not os.path.exists(self.module_info_file):
            self.status = 'error'
        else:
            self.config.read(self.module_info_file)

            self.version = self.__conf_get('version', self.version)
            self.friendly_name = self.__conf_get('name', self.name)
            self.run_as_user = None
            self.run_as_group = None

            if self.config.has_option('user', 'name'):
                self.run_as_user = self.config.get('user', 'name')

            if self.config.has_option('user', 'group'):
                self.run_as_group = self.config.get('user', 'group')

            if self.config.has_option('general', 'description'):
                self.description = self.config.get('general', 'description')
                self.short_description = self.description.strip().replace('\n', ' ')
                self.short_description = self.short_description.replace('\t', ' ')
                if len(self.short_description) > Module.MAX_SHORT_DESC_LENGTH:
                    self.short_description = self.short_description[0:Module.MAX_SHORT_DESC_LENGTH - 3] + '...'

    def __conf_get(self, name, val):
        if self.config.has_option('general', name):
            return self.config.get('general', name)
        else:
            return val


    def get_processes(self):

        if os.path.exists(self.context.db_directory + 'run/' + self.name + '.pid'):
            pid = False
            with open(self.context.db_directory + 'run/' + self.name + '.pid', 'r') as pidfile:
                pid = int(pidfile.read())

            if pid and os.path.exists('/proc/' + str(pid)):
                return [pid]
            else:
                print "Non-existing pid=" + str(pid)
                return []

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
            dir = context.get_modules_directory()
            for subdirectory in os.listdir(dir):    
                if os.path.isdir(dir+subdirectory):
                    modules[subdirectory] = self.get(context, subdirectory)
        except:
            print "Unable to list modules in "+context.get_modules_directory()
            return modules

        return modules

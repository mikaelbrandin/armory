__author__ = 'kra869'

import argparse
import os
import os.path
import ConfigParser


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


class ReadWriteRepositoryDirectory(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentError(self, "ReadWriteRepositoryDirectory:{0} is not a valid path".format(prospective_dir))

        if not os.access(prospective_dir, os.R_OK):
            raise argparse.ArgumentError(self, "ReadWriteRepositoryDirectory:{0} is not a readable directory".format(prospective_dir))

        if not os.path.exists(prospective_dir + os.path.sep + '.armory'):
            raise argparse.ArgumentError(self, "ReadWriteRepositoryDirectory:{0} is not a Armory".format(prospective_dir))

        if os.access(prospective_dir, os.W_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentError(self, "ReadWriteRepositoryDirectory:{0} is not a writable directory".format(prospective_dir))


class Context:
    def __init__(self):
        current_dir = os.getcwd()

        self.modules = Modules()

        self.home_directory = current_dir

        self.args_parser = argparse.ArgumentParser(prog='Armory')
        self.args_parser.add_argument('--debug', action='store_true', help='Enable debugging (mainly)')
        self.args_parser.add_argument('--directory', metavar='FILE', action=ReadWriteRepositoryDirectory, default=current_dir)
        self.sub_args_parsers = self.args_parser.add_subparsers(title='Armory commands', description='The commands available with Armory', help='Available Armory commmands')

    def register_command(self, cmd, command, **kwargs):
        if kwargs.get('help') is None:
            kwargs['help'] = '<No Help Available>'

        parser = self.sub_args_parsers.add_parser(cmd, help=kwargs.get('help'))
        parser.set_defaults(command=command)

        return parser

    def execute(self):
        args = self.args_parser.parse_args()

        self.home_directory = args.directory;

        args.command(args, self)

        return None

    def check_directories(self):
        pass


class Module:
    def __init__(self, module_directory):
        if not os.path.isdir(module_directory):
            raise NotImplementedError()

        self.module_directory = module_directory
        self.name = os.path.basename(module_directory)
        self.module_info_file = self.module_directory + '/' + self.name + '.info'
        self.version = '~'
        self.description = ''
        self.short_description = ''
        self.config = ConfigParser.SafeConfigParser()
        self.sync()

    def sync(self):
        if not os.path.exists(self.module_info_file):
            return False

        MAX_SHORT_DESC_LENGHT = 50

        self.config.read(self.module_info_file)

        self.version = self.config.get('general', 'version')
        if self.config.has_option('general', 'name'):
            self.name = self.config.get('general', 'name')

        if self.config.has_option('general', 'description'):
            self.description = self.config.get('general', 'description')
            self.short_description = self.description.strip().replace('\n', ' ')
            self.short_description = self.short_description.replace('\t', ' ')
            if len(self.short_description) > MAX_SHORT_DESC_LENGHT:
                self.short_description = self.short_description[0:MAX_SHORT_DESC_LENGHT - 3] + '...'

        return True


class Modules:
    def __init__(self):
        pass


    def get(self, module_directory):
        return Module(module_directory);

    def from_director(self, directory):
        modules = {}
        for subdirectory in os.listdir(directory + '/modules.d/'):
            modules[subdirectory] = self.get(directory + '/modules.d/' + subdirectory)

        return modules

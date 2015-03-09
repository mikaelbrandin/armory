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


class Context:
    def __init__(self):
        current_dir = os.getcwd()

        self.modules = Modules()

        self.args_parser = argparse.ArgumentParser(prog='Armory');
        self.args_parser.add_argument('--debug', action='store_true', help='Enable debugging (mainly)')
        self.args_parser.add_argument('--directory', metavar='FILE', action=ReadWriteDirectory, default=current_dir)
        self.sub_args_parsers = self.args_parser.add_subparsers(title='Armory commands', description='The commands available with Armory', help='Available Armory commmands')

    def register_command(self, cmd, command, **kwargs):
        if kwargs.get('help') is None:
            kwargs['help'] = '<No Help Available>'

        parser = self.sub_args_parsers.add_parser(cmd, help=kwargs.get('help'))
        parser.set_defaults(command=command)

        return parser

    def execute(self):
        args = self.args_parser.parse_args()
        args.command(args, self)

        return None


class Module:
    def __init__(self, module_directory):
        if not os.path.isdir(module_directory):
            raise NotImplementedError()

        self.module_directory = module_directory
        self.name = os.path.basename(module_directory)
        self.module_info_file = self.module_directory + '/' + self.name + '.info'
        self.version = '~'
        self.sync()

    def sync(self):
        if not os.path.exists(self.module_info_file):
            return False

        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.module_info_file)

        self.version = self.config.get('general', 'version');
        // self.name = self.config.has_option('general', 'name')

        return True


class Modules:
    def __init__(self):
        pass


    def get(self, module_directory):
        return Module(module_directory);

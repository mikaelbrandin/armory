__author__ = 'kra869'

import argparse
import os

def is_armory_central_repo_dir(dir):
    if not dir.endswith(os.sep):
        dir += os.sep

    if not os.path.isdir(dir):
        return False
    elif not os.access(dir, os.R_OK):
        return False
    elif not os.access(dir, os.W_OK):
        return False

    return True


class ReadWriteRepositoryDirectory(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not prospective_dir.endswith(os.sep):
            prospective_dir += os.sep

        if is_armory_central_repo_dir(prospective_dir):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentError(self, "ReadWriteRepositoryDirectory:{0} is not a armory directory".format(prospective_dir))


class Context:
    def __init__(self):
    
        self.repo_directory = os.getcwd() + os.sep;
        
        self.args_parser = argparse.ArgumentParser(prog='Armory Repository', description='Ex. armory-repo push ~/example-1.0.0.pack')
        self.args_parser.add_argument('--debug','-X', action='store_true', help='enable debugging information')
        self.args_parser.add_argument('--yes', action='store_true', help='confirm with yes to questions')
        self.args_parser.add_argument('--directory', '-D', metavar='DIR', action=ReadWriteRepositoryDirectory, default=self.repo_directory, help='directory for repository if other then current working directory')
        self.sub_args_parsers = self.args_parser.add_subparsers(title='Armory Repository commands', description='The commands available with Armory Repository', help='Available Armory Repository commmands')

    def register_command(self, cmd, command, **kwargs):
        if kwargs.get('help') is None:
            kwargs['help'] = '<No Help Available>'

        parser = self.sub_args_parsers.add_parser(cmd, help=kwargs.get('help'))
        parser.set_defaults(command=command)

        return parser
        
    def execute(self):
        args = self.args_parser.parse_args()
        self.repo_directory = args.directory
        
        if args.yes:
            os.environ['ARMORY_YES'] = 'YES'

        args.command(args, self)
        pass
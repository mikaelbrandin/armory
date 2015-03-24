__author__ = 'kra869'

import os
import configparser
from . import utils

def directory_filter(args):
    return os.getcwd();

def init(context):
    parser = context.register_command('init', command_init, help='Initialize a new repository', directory_filter=directory_filter)
    parser.add_argument('repository', metavar='REPOSITORY_URI', help="the repository uri")
    return None


def command_init(args, context):
    
    if not utils.confirm("Initialize repository in "+args.directory):
        print("Skipping initalization of local repository")
    
    db_directory = args.directory + '.armory'+os.sep
    modules_directory = args.directory + 'modules.d'+os.sep
    configuration_directory = args.directory + 'conf.d'+os.sep
    
    if not os.path.exists(db_directory):
        print("Create .armory directory")
        os.makedirs(db_directory)
        
    if not os.path.exists(modules_directory):
        print("Create modules.d directory")
        os.makedirs(modules_directory)
        
    if not os.path.exists(configuration_directory):
        print("Create conf.d directory")
        os.makedirs(configuration_directory)
        
    repositories = configparser.SafeConfigParser()
    repositories.read(db_directory+'repositories')
    
    #Modules
    if not repositories.has_section('modules'):
        repositories.add_section('modules');
    
    #Configurations
    if not repositories.has_section('configurations'):
        repositories.add_section('configurations');
    
    #Default repository
    repositories.set('modules', 'default', args.repository)
    repositories.set('configurations', 'default', args.repository)
    
    with open(db_directory+'repositories', "w+") as f:
        repositories.write(f);

    return None
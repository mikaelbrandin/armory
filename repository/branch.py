
import os
import ConfigParser

def init(context):
    parser = context.register_command('branch', command_branch, help='Initialize a new Armory repository')
    parser.add_argument('--create', '-C', action='store_true', help='create the following branches')
    parser.add_argument('--add', '-a', metavar='MODULE', nargs='+', help='add module/configuration to branch')
    parser.add_argument('branches', nargs='+', default=['main'])
    
def command_branch(args, context):
    if args.create:
        for branch in args.branches:
            create_branch(context, branch)
            
    if args.add:
        for branch in args.branches:
            add_to_branch(context, branch, args.add)
    pass
    
def add_to_branch(context, branch_name, modules):
    branch_info = context.repo_directory+branch_name+'.armory'
    
    info = ConfigParser.SafeConfigParser();
    info.read(branch_info)
    
    for module in modules:
        if not info.has_section('modules'):
            info.add_section('modules')
        
        info.set('modules', module, 'latest')
        
    with open(branch_info, 'w+') as f:
        info.write(f)
    
def create_branch(context, branch_name):

    branch_info = context.repo_directory+branch_name+'.armory'

    if not os.path.exists(branch_info):
        info = ConfigParser.SafeConfigParser()
        info.add_section('meta')
        info.set('meta', 'name', branch_name);
        with open(branch_info, 'w+') as f:
            info.write(f)
            
    pass

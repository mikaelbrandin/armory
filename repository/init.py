
import os
from . import utils
from . import branch as branches

def init(context):
    parser = context.register_command('init', command_init, help='Initialize a new Armory repository')
    parser.add_argument('--branches', '-b', default=['main'], nargs='*', help='initialize with the following branches')
    
def command_init(args, context):
    if not utils.confirm("Initialize repository in "+args.directory):
        print("ok, skipping repository initialization")
        return None
        
    if not os.path.exists(args.directory):
        os.makedirs(args.directory)
        
    if not os.path.exists(args.directory+'modules'+os.sep):
        os.makedirs(args.directory+'modules'+os.sep)
        
    if not os.path.exists(args.directory+'configurations'+os.sep):
        os.makedirs(args.directory+'configurations'+os.sep)
        
    if not os.path.exists(args.directory+'packages'+os.sep):
        os.makedirs(args.directory+'packages'+os.sep)
        
    if not os.path.exists(args.directory+'.armory'+os.sep):
        os.makedirs(args.directory+'.armory'+os.sep)
        
    if not os.path.exists(args.directory+'.armory'+os.sep+'REMOTE'):
        with open(args.directory+'.armory'+os.sep+'remote') as f:
            f.write("1.0.0");
        
    for branch in args.branches:
        branches.create_branch(context, branch)
        
    #with open(args.directory+'ARMORY', 'a'):
    #    os.utime(args.directory+'ARMORY', None)
    
        
    pass

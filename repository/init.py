
import os
import utils

def init(context):
    context.register_command('init', command_init, help='Initialize a new Armory repository')
    
def command_init(args, context):
    if not utils.confirm("Initialize repository in "+args.directory):
        print "Skipping initalization"
        return None
        
    if not os.path.exists(args.directory):
        os.makedirs(args.directory)
        
    if not os.path.exists(args.directory+'modules'+os.sep):
        os.makedirs(args.directory+'modules'+os.sep)
        
    if not os.path.exists(args.directory+'configurations'+os.sep):
        os.makedirs(args.directory+'configurations'+os.sep)
        
    if not os.path.exists(args.directory+'packages'+os.sep):
        os.makedirs(args.directory+'packages'+os.sep)
        
    with open(args.directory+'ARMORY', 'a'):
        os.utime(args.directory+'ARMORY', None)
    
        
    pass

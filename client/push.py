import clients
import utils
import glob
import os

def init(context):

    parser = context.register_command('push', command_push, help='Push commited packages')
    parser.add_argument('modules', metavar='MODULE', nargs='*')
    
    return None
    
def command_push(args, context):

    (modules, included) = utils.build_modules(context, args.modules);
    
    for mod_name in included:
        module = modules[mod_name];
        push(args, context, module)
    
    pass
    
def push(args, context, module):
    print module.name
    client = clients.create('file:///opt/armory_repo/')
    dir = context.db_directory+'commits'+os.sep+module.name+os.sep
    
    if not os.path.exists(dir):
        return False
    
    hash = utils.read_file(dir+module.name+'.commit')
    print hash+ " "+module.name
    client.push(module.name, dir+module.name+'.pack', hash)
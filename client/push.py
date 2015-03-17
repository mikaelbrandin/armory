import clients
import utils
import glob
import os
import shutil
import ConfigParser

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
    
    repos = ConfigParser.SafeConfigParser()
    repos.read(context.db_directory+'repositories')
    
    if not repos.has_option('modules', module.name):
        print "No remote repository for "+module.name
        return False
        
    repository_uri = repos.get('modules', module.name)
    
    client = clients.create(repository_uri)
    
    commit_dir = context.db_directory+'commits'+os.sep+module.name+os.sep
    if not os.path.exists(commit_dir):
        print "Nothing to push for "+module.name
        return False
    
    hash = utils.read_file(commit_dir+module.name+'.commit')
    print "Pushing "+hash+" "+module.name
    client.push(module.name, commit_dir+module.name+'.pack', hash)
    
    #Remove commit (as its be pushed)
    shutil.rmtree(commit_dir)
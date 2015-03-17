
import os
import utils
import tarfile
import tempfile
import ConfigParser
import shutil

def init(context):
    parser = context.register_command('push', command_push, help='Push package(s) into the Armory repository')
    parser.add_argument('packages', metavar='PACK', nargs='+', help='package(s) to push into repository')
    parser.add_argument('--remove', action='store_true', help='remove source package on complete')
    
def command_push(args, context):

    for pack in args.packages:
        push(pack, args, context)

def push(pack, args, context):

    tmp_dir = tempfile.mkdtemp()
    tmp_metainfo = tmp_dir+os.sep+'METAINF'
    tmp_manifest = tmp_dir+os.sep+'MANIFEST'

    metainfo = ConfigParser.SafeConfigParser()
    
    with tarfile.open(pack, 'r') as package:
        package.extract('METAINF', tmp_dir)
        package.extract('MANIFEST', tmp_dir)
        
        
    metainfo.read(tmp_metainfo)
    name = metainfo.get('meta', 'name');
    version = metainfo.get('meta', 'version')
    hash = metainfo.get('meta', 'hash')
    hash_type = metainfo.get('meta', 'hash_type')
    print name+'-'+version
    
    module_version_dir = context.repo_directory + 'modules' + os.sep +  name + os.sep + version + os.sep
    module_dir = context.repo_directory + 'modules' + os.sep +  name + os.sep
    if not os.path.exists(module_version_dir):
        os.makedirs(module_version_dir)

        
    shutil.copyfile(tmp_metainfo, module_version_dir+name+'.metainfo')
    shutil.copyfile(tmp_manifest, module_version_dir+name+'.manifest')
    
    shutil.copyfile(pack, context.repo_directory+'packages'+os.sep+name+'-'+version+'.pack')
    
    #VERSION index
    module_version_index = ConfigParser.SafeConfigParser()
    module_version_index.read(module_dir+'VERSIONS')
    
    if not module_version_index.has_section(version):
        module_version_index.add_section(version)
    
    module_version_index.set(version, 'hash', hash)
    module_version_index.set(version, 'hash_type', hash_type)
    
    with open(module_dir+'VERSIONS', 'w+') as f:
        module_version_index.write(f);
    
    #MODULES index
    modules_index = ConfigParser.SafeConfigParser()
    modules_index.read(context.repo_directory+'MODULES')
    
    if not modules_index.has_section(name):
        modules_index.add_section(name)
    
    modules_index.set(name, 'hash', hash)
    modules_index.set(name, 'version', version)
    modules_index.set(name, 'hash_type', hash_type)
    with open(context.repo_directory+'MODULES', 'w+') as f:
        modules_index.write(f);
    
        
    shutil.rmtree(tmp_dir)
    
    if args.remove:
        os.remove(pack)
    
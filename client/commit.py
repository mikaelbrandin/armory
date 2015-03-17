__author__ = 'kra869'

import hashlib
import os
import utils
import tarfile
import shutil
import ConfigParser
import datetime

class CommitException(BaseException):
    def __init__(self, msg):
        self.msg = msg


def init(context):
    parser = context.register_command('commit', command_commit, help='Commit a module')
    parser.add_argument('modules', metavar='MODULE', nargs='*')

    return None


def command_commit(args, context):
    (modules, included) = utils.build_modules(context, args.modules)
    
    for mod_name in included:
        commit(args, context, modules[mod_name])
    
    
def commit(args, context, module):
    print module.name+"/"+module.friendly_name + " from " + module.module_directory
    
    info = ConfigParser.SafeConfigParser()
    info.read(module.module_info_file)
    
    if not info.has_option('general', 'version'):
        raise CommitException('No version, please provide a valid version tag in module .info file')
        
    version = info.get('general', 'version')
    
    dir = context.db_directory+'commits'+os.sep
    
    if not os.path.exists(dir):
        os.makedirs(dir);

    tmp_pack = dir+'.'+module.name+'.pack'
    tmp_manifest = dir+'.'+module.name+'.manifest'
    tmp_metainfo = dir+'.'+module.name+'.metainfo'
        
    package_hash = hashlib.sha1()
    with open(tmp_manifest, 'w+') as manifest:
        for root, dirs, files in os.walk(module.module_directory, topdown=False):
            for name in files:
                f = os.path.join(root, name)
                rel = os.path.relpath(f, module.module_directory)
                hv = utils.hash_file(f)
                print hv + " " + rel
                package_hash.update(rel + " sha1 " + hv)
                manifest.write(rel + " sha1 " + hv+"\n")

    package_hash = package_hash.hexdigest();
    
    metainfo = ConfigParser.SafeConfigParser()
    metainfo.add_section('meta')
    metainfo.set('meta', 'name', module.name)
    metainfo.set('meta', 'friendly_name', module.friendly_name)
    metainfo.set('meta', 'hash', package_hash)
    metainfo.set('meta', 'hash_type', 'sha1')
    metainfo.set('meta', 'package_type', 'module')
    metainfo.set('meta', 'built', str(datetime.datetime.now()))
    metainfo.set('meta', 'built_by', os.getlogin())
    metainfo.set('meta', 'version', version);
    
    with open(tmp_metainfo, 'w+') as f:
        metainfo.write(f)
                
    with tarfile.open(tmp_pack, 'w') as pack:
        for entry in os.listdir(module.module_directory):
            pack.add(module.module_directory+entry, arcname=entry)
        pack.add(tmp_manifest, 'MANIFEST')
        pack.add(tmp_metainfo, 'METAINF')

    commit_dir = dir+module.name+os.sep
    
    if os.path.exists(commit_dir):
        shutil.rmtree(commit_dir);
    
    os.mkdir(commit_dir);
    
    os.rename(tmp_manifest, commit_dir+module.name+'.manifest');
    os.rename(tmp_pack, commit_dir+module.name+'.pack');
    os.rename(tmp_metainfo, commit_dir+module.name+'.metainfo');
    
    with open(commit_dir+module.name+'.commit', 'w+') as f:
        f.write(package_hash)
    
    pass



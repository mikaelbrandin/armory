__author__ = 'kra869'

import hashlib
import os
import utils
import tarfile
import shutil
import ConfigParser
import datetime
import context as ctx
import tempfile
import sys

class PackageException(BaseException):
    def __init__(self, msg):
        self.msg = msg


def init(context):
    parser = context.register_command('package', command_package, help='Package a module or configurations')
    
    parser.add_argument('sources', metavar='DIRECTORY', nargs='+', help='TBD')
    parser.add_argument('--file', '-f', metavar='FILE', help='Write package to FILE')

    return None

def command_package(args, context):
    
    modules = context.modules.from_context(context)
    
    for src in args.sources:
        if src in modules:
            package_module(args, context, modules[src])
        elif os.path.exists(src) and os.path.isdir(src):
            if not src.endswith(os.sep):
                src = src + os.sep
                
            module = ctx.Module(src, context)
            package_module(args, context, module)
        else:
            raise PackageException("Missing source, nothing to package")
            
    
    #for mod_name in included:
    #    commit(args, context, modules[mod_name])
    
    
def package_module(args, context, module):
    
    #Read module .info file
    info = ConfigParser.SafeConfigParser()
    info.read(module.module_info_file)
    
    version = info.get('general', 'version')
    if not info.has_option('general', 'version'):
        raise PackageException('No version, please provide a valid version tag in module .info file for '+module.name)
    
    print module.name + "("+version+") from " + module.module_directory
    
    #Create temporary directory
    dir = tempfile.mkdtemp('am-package') + os.sep
    
    if not os.path.exists(dir):
        os.makedirs(dir);

    tmp_pack = dir+module.name+'.pack'
    tmp_manifest = dir+'MANIFEST'
    tmp_metainfo = dir+'METAINF'
    
    #Create MANIFEST
    package_hash = hashlib.sha1()
    with open(tmp_manifest, 'w+') as manifest:
        for root, dirs, files in os.walk(module.module_directory, topdown=False):
            for name in files:
                f = os.path.join(root, name)
                rel = os.path.relpath(f, module.module_directory)
                hv = utils.hash_file(f)
                print hv + "\t" + rel
                package_hash.update(rel + " sha1 " + hv)
                manifest.write(rel + " sha1 " + hv+"\n")

    package_hash = package_hash.hexdigest();
    
    #Create METAINF
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
    
    #Last create .pack file in temporary dir
    with tarfile.open(tmp_pack, 'w') as pack:
        for entry in os.listdir(module.module_directory):
            pack.add(module.module_directory+entry, arcname=entry)
        pack.add(tmp_manifest, 'MANIFEST')
        pack.add(tmp_metainfo, 'METAINF')
    
    #Copy file to cwd or argument --file destination
    dest = os.getcwd()+os.sep+module.name+'-'+version+'.pack'
    if 'file' in args and args.file != None:
        dest = args.file
        
    shutil.copyfile(tmp_pack, dest)

    #Remove temporary dir
    shutil.rmtree(dir)
    
    pass



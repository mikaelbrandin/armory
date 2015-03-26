import configparser
import tempfile
import shutil
import os
import tarfile

from . import clients


def init(context):
    parser = context.register_command('pull', command_pull, help='Pull a remote package from remote repository')
    parser.add_argument('modules', metavar='MODULE', nargs='+')
    parser.add_argument('--repository', metavar='REPOSITORY_URI', help='A remote repository', default=None);

    parser = context.register_command('install', command_install, help='Install package from file')
    parser.add_argument('packages', metavar='PACKAGE', nargs='+')

    return None


def command_pull(args, context):
    repository_uri = args.repository

    repositories = configparser.SafeConfigParser()
    repositories.read(context.db_directory + 'repositories')

    if repository_uri is None:
        repository_uri = repositories.get('modules', 'default')

    for mod_name in args.modules:
        if repositories.has_option('modules', mod_name):
            package = pull(mod_name, repositories.get('modules', mod_name), context, args)
        else:
            package = pull(mod_name, repository_uri, context, args)

        install(package, args, context);
        os.remove(package)


def command_install(args, context):
    for package_file in args.packages:
        install(package_file, args, context);


def pull(name, repository_uri, context, args):
    client = clients.create(repository_uri);
    package = context.db_directory + '/' + name + '-latest.pack'
    
    if '.' in name:
        client.pull('configurations', name, 'latest', package);
    else:
        client.pull('modules', name, 'latest', package)

    return package


def install(package_file, args, context):
    tmp_dir = tempfile.mkdtemp()
    tmp_metainfo = tmp_dir + os.sep + 'METAINF'
    tmp_manifest = tmp_dir + os.sep + 'MANIFEST'

    metainfo = configparser.SafeConfigParser()

    with tarfile.open(package_file, 'r') as package:
        package.extract('METAINF', tmp_dir)
        package.extract('MANIFEST', tmp_dir)

    metainfo.read(tmp_metainfo)
    name = metainfo.get('meta', 'name')
    version = metainfo.get('meta', 'version')
    hash = metainfo.get('meta', 'hash')
    hash_type = metainfo.get('meta', 'hash_type')

    module_dir = context.get_module_directory(name, version)
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)
    else:
        print("Uninstalling " + name + "(same version) from " + module_dir)
        shutil.rmtree(module_dir)
        os.makedirs(module_dir)

    print("Install " + name + " " + version + " to " + module_dir)

    with tarfile.open(package_file, 'r') as package:
        package.extractall(module_dir)

    os.remove(module_dir + 'MANIFEST')
    os.remove(module_dir + 'METAINF')

    print(context.get_module_directory(name, 'latest') + " -> " + module_dir)

    os.symlink(os.path.dirname(module_dir), os.path.dirname(context.get_module_directory(name, 'latest')))

    # archive_dir = context.db_directory + 'archive' + os.sep
    # if not os.path.exists(archive_dir):
    # os.makedirs(archive_dir)

    # shutil.copyfile(package_file, archive_dir + name + '-' + version + '.orig.pack')
    shutil.rmtree(tmp_dir)
    
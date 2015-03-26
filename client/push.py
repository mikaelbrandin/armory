import os
import shutil
import tempfile
import tarfile

from . import clients
import configparser
from . import exceptions


class PushException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(PushException, self).__init__(msg)


def init(context):
    parser = context.register_command('push', command_push, help='Push commited packages')
    parser.add_argument('repository', metavar='URL', help='repository uri')
    parser.add_argument('packs', metavar='FILE', nargs='+', help='package file (module or configuration)')

    return None


def command_push(args, context):
    for pack_file in args.packs:
        if os.path.exists(pack_file) and pack_file.endswith('.pack'):
            push(args, context, pack_file)
        else:
            raise PushException("No such file: " + pack_file)

    pass


def push(args, context, pack_file):
    tmp_dir = tempfile.mkdtemp('am-push') + os.sep
    tmp_pack_file = tmp_dir + 'tmp.pack'
    tmp_manifest = tmp_dir + 'MANIFEST'
    tmp_metainfo = tmp_dir + 'METAINF'

    with tarfile.open(pack_file, 'r') as pack:
        pack.extract('MANIFEST', tmp_dir)
        pack.extract('METAINF', tmp_dir)

    metainfo = configparser.SafeConfigParser()
    metainfo.read(tmp_metainfo)

    pack_name = metainfo.get('meta', 'name')
    pack_version = metainfo.get('meta', 'version')
    pack_hash = metainfo.get('meta', 'hash')
    pack_type = metainfo.get('meta', 'type')

    # if not (repos.has_option('modules', module_name) or repos.has_option('modules', 'default')):
    # print "Unable to resolve remote repository for "+context.home_directory
    # shutil.rmtree(tmp_dir)
    # return False

    repository_uri = args.repository

    # if repos.has_option('modules', 'default'):
    # repository_uri = repos.get('modules', 'default')

    # if repos.has_option('modules', module_name):
    # repository_uri = repos.get('modules', module_name)


    print(pack_name + "( " + pack_version + " ) -> " + repository_uri)
    client = clients.create(repository_uri)

    # Push file
    client.push(pack_name, pack_file, pack_hash)

    # Clean Up
    shutil.rmtree(tmp_dir)
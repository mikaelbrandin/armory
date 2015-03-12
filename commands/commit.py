__author__ = 'kra869'

import hashlib
import os

BLOCKSIZE = 65536


def init(context):
    parser = context.register_command('commit', command_commit, help='Commit a module')
    parser.add_argument('module', metavar='MODULE')
    parser.add_argument('environment', metavar='ENV', nargs='*')

    parser = context.register_command('push', command_push, help='Push commited packages')
    return None


def command_commit(args, context):
    module = context.modules.get(context, args.module)
    for root, dirs, files in os.walk(module.module_directory, topdown=False):

        for name in files:
            f = os.path.join(root, name)
            rel = os.path.relpath(f, module.module_directory)
            print rel + " sha1 " + __hash(f)


def __hash(file_path):
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)

    return hasher.hexdigest()


def command_push(args, context):
    pass
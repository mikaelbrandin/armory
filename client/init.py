__author__ = 'kra869'


def init(context):
    parser = context.register_command('init', command_init, help='Initialize a new repository')
    return None


def command_init(args, context):
    print args.directory

    return None
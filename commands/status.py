__author__ = 'kra869'


def init(context):
    parser = context.register_command('status', command_status, help='Show status information')
    return None


def command_status(args, context):
    print args.directory

    return None
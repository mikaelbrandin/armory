__author__ = 'kra869'

import os


def init(context):
    parser = context.register_command('status', command_status, aliases=['ps', 'stat'], help='Show status information for one or more modules')
    parser.add_argument('modules', metavar='MODULE', nargs='*')
    return None


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def command_status(args, context):
    modules = context.modules.from_context(context)

    if len(args.modules) == 0 or (len(args.modules) == 1 and args.modules[0] == 'all'):
        args.modules = list(modules.keys())

    print("-----")
    print(" Environment: " + context.environment)
    print("  Repository: " + context.home_directory)
    print("   Directory: " + args.directory)
    print("        User: " + context.user_directory)
    print("-----")

    for mod in args.modules:
        display_status(args, context, modules[mod])

    return None


def fill_width(n):
    print('=' * n)


def display_status(args, context, module):
    pids = module.get_processes()

    stat = 'stopped'
    if len(pids) > 0:
        stat = 'running'

    print("{name:30} [{status}]".format(name=module.name + "-" + module.version, version=module.version, status=stat))
    for pid in pids:
        if pid == -1:
            continue

        if not os.path.exists('/proc/' + str(pid)):
            print(str(pid) + " not found in /proc == dead pid")
            continue

        stat = open('/proc/' + str(pid) + '/stat', 'r').read().split()
        # memstat = open('/proc/' + str(pid) + '/statm', 'r').read().split()
        # total_mem=sizeof_fmt(int(memstat[0]), 'B')
        print("  {pid} {name:10}".format(pid=pid, name=stat[1].strip()))

    print("---")
    pass
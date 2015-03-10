__author__ = 'kra869'

import os
import subprocess


def init(context):
    parser = context.register_command('start', command_start, help='Start a service')
    parser.add_argument('services', nargs='+')
    return None


def command_start(args, context):
    modules = context.modules.from_director(args.directory)

    if len(args.services) == 1 and args.services[0] == 'all':
        args.services = modules.keys()

    for service in args.services:
        start(args, context, modules[service])

    return None


def start(args, context, module):
    env = os.environ.copy()

    context.check_directories()

    env['ARMORY_HOME'] = args.directory
    env['ARMORY_RUN_DIRECTORY'] = args.directory + '/.armory/run/'

    subprocess.Popen(args.directory + '/modules.d/' + module.name + '/start', env=env)
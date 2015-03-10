__author__ = 'kra869'

import os
import subprocess


def init(context):
    parser = context.register_command('start', command_start, help='Start a service')
    parser.add_argument('services', nargs='+')
    return None


def command_start(args, context):
    modules = context.modules.from_context(context)

    context.check_directories()

    if len(args.services) == 1 and args.services[0] == 'all':
        args.services = modules.keys()

    for service in args.services:
        start(args, context, modules[service])

    return None


def start(args, context, module):
    env = os.environ.copy()

    env.update(context.env)

    env['ARMORY_MODULE_DIRECTORY'] = context.get_module_directory(module.name)
    env['ARMORY_MODULE_CONF_DIRECTORY'] = context.get_config_directory(module.name, env['ARMORY_ENV'])

    subprocess.Popen(module.module_directory + '/start', env=env)
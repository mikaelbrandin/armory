__author__ = 'kra869'

import os
import subprocess
import utils


def init(context):
    parser = context.register_command('start', command_start, help='Start one or more module')
    parser.add_argument('modules', metavar='MODULE', nargs='*')

    parser = context.register_command('stop', command_stop, help='Stop one or more module')
    parser.add_argument('modules', metavar='MODULE', nargs='*')
    return None


def init_command(args, context):

    (modules, included) = utils.build_modules(context, args.modules);
    args.modules = included;

    context.check_directories()

    return modules


def command_start(args, context):
    modules = init_command(args, context)

    for module in args.modules:
        start(args, context, modules[module])

    return None


def command_stop(args, context):
    modules = init_command(args, context)

    for module in args.modules:
        stop(args, context, modules[module])

    return None


def start(args, context, module):
    if not os.path.exists(module.module_directory + '/stop'):
        print "Unable to start '" + module.name + "', no start script"
        return False

    pids = module.get_processes()

    if len(pids) > 0:
        print module.name + " already started"
        return True

    print "Starting " + module.name

    env = os.environ.copy()
    env.update(context.env)

    env['ARMORY_MODULE_DIRECTORY'] = context.get_module_directory(module.name)
    env['ARMORY_MODULE_CONF_DIRECTORY'] = context.get_config_directory(module.name, env['ARMORY_ENV'])

    subprocess.call(module.module_directory + '/start', env=env)
    return True


def stop(args, context, module):
    if not os.path.exists(module.module_directory + '/stop'):
        print "Unable to stop " + module.name + " no stop script"
        return False

        if len(pids) == 0:
            print module.name + " not running"
            return True

    env = os.environ.copy()
    env.update(context.env)

    print "Stopping " + module.name

    env['ARMORY_MODULE_DIRECTORY'] = context.get_module_directory(module.name)
    env['ARMORY_MODULE_CONF_DIRECTORY'] = context.get_config_directory(module.name, env['ARMORY_ENV'])

    subprocess.call(module.module_directory + '/stop', env=env)
    return True
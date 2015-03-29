__author__ = 'kra869'

import os
import subprocess
import sys
import pwd

from . import exceptions
from . import utils
from . import configurations


class StartException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(StartException, self).__init__(msg)


class StopException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(StopException, self).__init__(msg)


def init(context):
    parser = context.register_command('start', command_start, help='Start one or more module')
    parser.add_argument('modules', metavar='MODULE', nargs='*')

    parser = context.register_command('stop', command_stop, help='Stop one or more module')
    parser.add_argument('modules', metavar='MODULE', nargs='*')
    return None


def command_start(args, context):
    (modules, included) = utils.build_modules(context, args.modules)

    effective_uid = os.geteuid()

    # Check for root
    if effective_uid != 0:
        raise StartException("Please run with root as effective user")

    default_pw = pwd.getpwnam(os.getlogin())
    uid = default_pw.pw_uid
    gid = default_pw.pw_gid

    for name in included:
        module = modules[name]

        if module.run_as_user is not None:
            pw = pwd.getpwnam(module.run_as_user)
            override_uid = pw.pw_uid
            override_gid = pw.pw_gid
            try:
                start(args, context, module, override_uid, override_gid)
            except exceptions.ArmoryException as e:
                e.print_message()
        else:
            try:
                start(args, context, module, uid, gid)
            except exceptions.ArmoryException as e:
                e.print_message()

    return None


def command_stop(args, context):
    (modules, included) = utils.build_modules(context, args.modules)

    effective_uid = os.geteuid()

    # Check for root
    if effective_uid != 0:
        raise StopException("Please run with root as effective user")

    for module in included:
        stop(args, context, modules[module])

    return None


def demote(uid, gid):
    def result():
        os.setgid(gid)
        os.setuid(uid)
        os.setpgrp()

    return result


def start(args, context, module, uid, gid):
    pids = module.get_processes()
    # TODO: Check that process id is active!

    if len(pids) > 0:
        print(module.name + " [running]")
        return True

    print("starting " + module.name)

    env = os.environ.copy()
    env.update(context.env)
    env['ARMORY_MODULE_DIRECTORY'] = context.get_module_directory(module.name, 'latest')
    env['ARMORY_MODULE_CONF_DIRECTORY'] = context.get_config_directory(configurations.ConfigName(module.name, env['ARMORY_BRANCH']), 'latest')

    if os.path.exists(module.module_directory + 'run'):
        start_with_runscript(args, context, module, env, uid, gid)
    elif os.path.exists(module.module_directory + 'start'):
        start_with_startscript(args, context, module, env, uid, gid)
    else:
        raise StartException("Unable to start, missing start scripts")

    # subprocess.call(module.module_directory + 'start', env=env)
    return True


def start_with_runscript(args, context, module, env, uid, gid):
    _proc = subprocess.Popen(
        ['nohup', module.module_directory + 'run'],
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
        preexec_fn=demote(uid, gid)
    )

    if not os.path.exists(context.db_directory + 'run' + os.sep):
        os.makedirs(context.db_directory + 'run' + os.sep)

    # print "run pid={pid}".format(pid=_proc.pid)
    with open(context.db_directory + 'run' + os.sep + module.name + '.pid', "w+") as pidfile:
        pidfile.write(str(_proc.pid))


def start_with_startscript(args, context, module, env, uid, gid):
    proc = subprocess.Popen(
        ['nohup', module.module_directory + 'start'],
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
        preexec_fn=demote(uid, gid)
    )
    # print "start pid={pid}".format(pid=proc.pid)


def stop(args, context, module):
    pids = module.get_processes()

    if len(pids) == 0:
        print(module.name + " [stopped]")
        return True

    if not os.path.exists(module.module_directory + '/stop'):
        print("Unable to stop " + module.name + " no stop script")
        return False

    env = os.environ.copy()
    env.update(context.env)
    env['ARMORY_MODULE_DIRECTORY'] = context.get_module_directory(module.name)
    env['ARMORY_MODULE_CONF_DIRECTORY'] = context.get_config_directory(module.name, env['ARMORY_ENV'])

    if os.path.exists(context.db_directory + 'run' + os.sep + module.name + '.pid'):
        print(module.name + "[stopping]")
        with open(context.db_directory + 'run' + os.sep + module.name + '.pid', 'r') as pidfile:
            pid = int(pidfile.read())
            os.kill(pid)

        os.remove(context.db_directory + 'run' + os.sep + module.name + '.pid')
    elif os.path.exists(module.module_directory + 'stop'):
        print(module.name + "[stopping]")
        subprocess.call(module.module_directory + 'stop', env=env)
    else:
        raise StopException("Missing stop scripts")

    return True
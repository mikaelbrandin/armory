__author__ = 'mikael.brandin@devolver.se'

import argparse
from collections import namedtuple

ConfigName = namedtuple('ConfigName', ['branch', 'module'])


class ConfigurationNamingException(BaseException):
    def __init__(self, msg):
        self.msg = msg
        pass


def to_name(value):
    _value = value.split('.')

    if not len(_value) is 2:
        raise ConfigurationNamingException("Unable to parse configuration name, excepts <BRANCH>.<MODULE> ex. dev.moduleA")

    return ConfigName(branch=_value[0], module=_value[1])


class ConfigAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, map(to_name, values))


def init(context):
    parser = context.register_command('configuration', command_config, help='interact with module metainfo and module data')
    parser.add_argument('configs', metavar='CONF', nargs='*', action=ConfigAction, help='Configuration name ex. dev.moduleA')
    parser.add_argument('--create', '-C', action='store_true', help='create module configuration in repository')
    return None


def command_config(args, context):
    if args.create:
        for conf in args.configs:
            create(conf, args, context)
    else:
        for conf in args.configs:
            info(conf, {}, args, context)

    pass


def create(conf, args, context):
    print conf.branch + '.' + conf.module
    pass


def info(conf, available_modules, args, context):
    pass

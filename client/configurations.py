__author__ = 'mikael.brandin@devolver.se'

import argparse
from collections import namedtuple
from client import output
import os
import configparser
import datetime

ConfigName = namedtuple('ConfigName', ['branch', 'module'])

#Constants
META_SECTION = 'general'

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
        setattr(namespace, self.dest, list(map(to_name, values)))


def init(context):
    parser = context.register_command('configuration', command_config, aliases=['conf'], help='interact with module metainfo and module data')
    parser.add_argument('configs', metavar='CONF', nargs='*', action=ConfigAction, help='Configuration name ex. dev.moduleA')
    parser.add_argument('--create', '-C', action='store_true', help='create module configuration in repository')
    return None


def command_config(args, context):
    if args.create:
        for conf in args.configs:
            if create(conf, args, context):
                output.ok();
    else:
        for conf in args.configs:
            info(conf, {}, args, context)

    pass


def create(conf, args, context):
    output.msgln(conf.branch + '.' + conf.module+ ":")
    
    _dir = context.get_configs_directory()
    
    if not os.path.exists(_dir):
        os.makedirs(_dir)
        
    if os.path.exists(_dir + conf.module + os.sep + conf.branch + os.sep):
        output.error(conf.branch+" branch already exists");
        return False

    version = "1.0.0"
    conf_dir        = _dir + conf.module + os.sep + conf.branch + os.sep + version + os.sep
    conf_dir_latest = _dir + conf.module + os.sep + conf.branch + os.sep + 'latest'
    os.makedirs(conf_dir)
    name = conf.branch+"."+conf.module
    
    info = configparser.SafeConfigParser()
    info.add_section(META_SECTION);
    info.set(META_SECTION, "name", name)
    info.set(META_SECTION, "version", version)
    info.set(META_SECTION, "created", str(datetime.datetime.now()))
    info.set(META_SECTION, "type", "configuration")
    
    with open(conf_dir + name + '.info', "w+") as f:
        info.write(f)
        
    os.symlink(conf_dir, conf_dir_latest)

    return True


def info(conf, available_modules, args, context):
    pass
    
class Configuration:
    MAX_SHORT_DESC_LENGTH = 50

    def __init__(self, name, conf_directory, context):
        self.context = context

        self.conf_directory = conf_directory
        self.name = name
        self.conf = to_name(name)

        if not os.path.exists(conf_directory + self.name + '.info'):
            raise ModuleException("Not an valid module: missing .info file in " + module_directory)

        self.friendly_name = self.name
        self.conf_info_file = self.conf_directory + self.name + '.info'

        self.version = '~'
        self.description = '<no description>'
        self.short_description = '<no description>'
        self.config = configparser.SafeConfigParser()
        self.status = "ok"

        if not os.path.exists(self.conf_info_file):
            self.status = 'error'
        else:
            self.config.read(self.conf_info_file)

            self.version = self.__conf_get('version', self.version)
            self.friendly_name = self.__conf_get('name', self.name)

            if self.config.has_option('general', 'description'):
                self.description = self.config.get('general', 'description')
                self.short_description = self.description.strip().replace('\n', ' ')
                self.short_description = self.short_description.replace('\t', ' ')
                if len(self.short_description) > Module.MAX_SHORT_DESC_LENGTH:
                    self.short_description = self.short_description[0:Module.MAX_SHORT_DESC_LENGTH - 3] + '...'

    def __conf_get(self, name, val):
        if self.config.has_option('general', name):
            return self.config.get('general', name)
        else:
            return val

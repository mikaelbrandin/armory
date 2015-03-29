__author__ = 'mikael.brandin@devolver.se'
import os
import os.path
import configparser

from . import utils
from . import exceptions
from . import output

META_SECTION = 'general'

def init(context):
    parser = context.register_command('module', command_module, aliases=['mod'], help='interact with module metainfo and module data')
    parser.add_argument('modules', metavar='MODULE', nargs='*')
    parser.add_argument('--create', '-C', action='store_true', help='create module in repository')
    parser.add_argument('--list', '-l', action='store_true', help='list modules and versions')
    parser.add_argument('--version', '-v', help='indicate version of operation (--create, ...)')
    return None


def command_module(args, context):
    _modules = context.modules.from_context(context)

    if args.create:
        for module_name in args.modules:
            command_module_create(module_name, args, context)
    elif args.list:
        command_list_modules(args, context)
    else:
        # all and empty eq. all modules
        if len(args.modules) == 0:
            args.modules = list(_modules.keys())
        elif len(args.modules) > 0 and args.modules[0] == 'all':
            args.modules = list(_modules.keys())

        for module_name in args.modules:
            info(module_name, _modules, args, context)


def command_module_create(module_name, args, context):

    version = 'latest'
    if 'version' in args:
        version = args.version

    if os.path.exists(context.get_module_directory(module_name, version)):
        raise ModuleException('Module exists: '+module_name+'-'+version)
        
    if version == 'latest':
        version = '1.0.0'
 
    create(module_name, version, context)
    
    pass

def create(module_name, version, context):
    dir = context.get_module_directory(module_name, version)
    
    #Create module directory
    os.makedirs(dir)
    
    #Create .info
    _info = configparser.SafeConfigParser()
    _info.add_section('general')
    _info.set('general', 'name', module_name)
    _info.set('general', 'version', version)
    
    with open(dir + module_name + '.info', "w+") as f:
        _info.write(f)
        
    _versions = context.modules.get_versions(context, module_name)

    return None

def command_list_modules(args, context):
    _modules = context.modules.from_context(context)
    
    for _name in _modules:
        _module = _modules[_name]
        _versions = context.modules.get_versions(context, _module.name)
        
        for _version in _versions:
            output.msgln(_module.name, label=_version)
        
    
def info(module_name, available_mods, args, context):
    _module = available_mods[module_name]
    
    output.msgln(module_name + " (" + _module.version + ")", label=_module.status)

    pass

class ModuleException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(ModuleException, self).__init__(msg)

class Module:
    MAX_SHORT_DESC_LENGTH = 50

    def __init__(self, module_name, module_directory, context):
        self.context = context

        self.module_directory = module_directory
        self.name = module_name

        if not os.path.exists(module_directory + self.name + '.info'):
            raise ModuleException("Not an valid module: missing .info file in " + module_directory)

        self.friendly_name = self.name
        self.module_info_file = self.module_directory + self.name + '.info'

        self.version = '~'
        self.description = '<no description>'
        self.short_description = '<no description>'
        self.config = configparser.SafeConfigParser()
        self.status = "ok"

        if not os.path.exists(self.module_info_file):
            self.status = 'error'
        else:
            self.config.read(self.module_info_file)

            self.version = self.__conf_get('version', self.version)
            self.friendly_name = self.__conf_get('name', self.name)
            self.run_as_user = None
            self.run_as_group = None

            if self.config.has_option('user', 'name'):
                self.run_as_user = self.config.get('user', 'name')

            if self.config.has_option('user', 'group'):
                self.run_as_group = self.config.get('user', 'group')

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

    def get_processes(self):

        if os.path.exists(self.context.db_directory + 'run/' + self.name + '.pid'):
            _pid = False
            with open(self.context.db_directory + 'run/' + self.name + '.pid', 'r') as pid_file:
                _pid = int(pid_file.read())

            if _pid and os.path.exists('/proc/' + str(_pid)):
                return [_pid]
            else:
                return []

        elif os.path.exists(self.module_directory + 'ps'):
            return [int(x) for x in utils.cmd(self.module_directory + 'ps').splitlines()]
        else:
            return []

    def sync(self):
        if not os.path.exists(self.module_info_file):
            return False

        self.config.read(self.module_info_file)

        self.version = self.__conf_get('version', self.version)
        self.friendly_name = self.__conf_get('name', self.name)

        if self.config.has_option('general', 'description'):
            self.description = self.config.get('general', 'description')
            self.short_description = self.description.strip().replace('\n', ' ')
            self.short_description = self.short_description.replace('\t', ' ')
            if len(self.short_description) > Module.MAX_SHORT_DESC_LENGTH:
                self.short_description = self.short_description[0:Module.MAX_SHORT_DESC_LENGTH - 3] + '...'

        return True


class Modules:
    def __init__(self):
        pass

    def get(self, context, module_name, version):
        return Module(module_name, context.get_module_directory(module_name, version), context)
        
    def get_versions(self, context, module_name):
        _dir = context.get_modules_directory()
        _dir += module_name + os.sep
        
        _results = []
        for module_directory in os.listdir(_dir):
            if module_directory == 'latest':
                continue
                
            _results.append(module_directory)
            
        return _results

    def from_context(self, context):
        modules = {}
        # try:
        _dir = context.get_modules_directory()
        for module_name in os.listdir(_dir):
            if os.path.isdir(_dir + module_name):
                try:
                    modules[module_name] = self.get(context, module_name, 'latest')
                except ModuleException:
                    print("Broken module: " + module_name)
        # except BaseException as e:
        # print "Unable to list modules in " + context.get_modules_directory()
        # return modules

        return modules


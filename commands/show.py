__author__ = 'kra869'

import os
import os.path

available_sections = ['mods', 'configs']


def init(context):
    parser = context.register_command('show', command_show, help='Show  information about armory repository')
    global available_sections
    parser.add_argument('sections', nargs='+', choices=available_sections)
    return None


def command_show(args, context):
    for section in args.sections:
        if section == 'mods':
            return command_show_mods(args, context)
        elif section == 'configs':
            return command_show_config(args, context)

    return None


def command_show_mods(args, context):
    modules = {}
    for subdirectory in os.listdir(args.directory + '/modules.d/'):
        modules[subdirectory] = context.modules.get(args.directory + '/modules.d/' + subdirectory)

    for name, module in modules.iteritems():
        print module.name

    return None


def command_show_config(args, context):
    return None

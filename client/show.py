__author__ = 'kra869'

available_sections = ['modules', 'mods', 'configuration', 'config']


def init(context):
    parser = context.register_command('show', command_show, help='Show  information about armory repository')
    global available_sections
    parser.add_argument('sections', nargs='+', choices=available_sections)
    return None


def command_show(args, context):
    for section in args.sections:
        if section == 'mods' or section == 'modules':
            return command_show_mods(args, context)
        elif section == 'configs' or section == 'configuration':
            return command_show_config(args, context)

    return None


def command_show_mods(args, context):
    modules = context.modules.from_context(context)

    print "{status:8} {name:30} {version:20} {description:50}".format(name="NAME", version="VERSION", status="STATUS", description="DESCRIPTION")
    for name, module in modules.iteritems():
        print "[{status:^6}] {name:30} {version:20} {description:50}".format(name=module.name, version=module.version, status=module.status, description=module.short_description)

    return None


def command_show_config(args, context):
    return None

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
    modules = context.modules.from_directory(args.directory)

    print "{status:6} {name:30} {version:20} {description:50}".format(name="Name", version="Version", status="Status", description="Description")

    for name, module in modules.iteritems():
        print "[{status:^4}] {name:30} {version:20} {description:50}".format(name=name, version=module.version, status="ok", description=module.short_description)

    return None


def command_show_config(args, context):
    return None

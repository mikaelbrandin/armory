__author__ = 'kra869'

import subprocess
import hashlib
import os

from ar.semantic_version import Spec as VersionSpec
from . import output


def register_scheme(scheme):
    for method in [s for s in dir(urlparse) if s.startswith('uses_')]:
        getattr(urlparse, method).append(scheme)


def cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return out


def hash_file(file_path):
    BLOCKSIZE = 65000
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)

    return hasher.hexdigest()


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def build_modules(context, module_names=[], **kwargs):
    modules = context.modules.from_context(context)

    if len(module_names) > 0 and not (len(module_names) == 1 and module_names[0] == 'all'):
        return modules, module_names

    if len(module_names) == 1 and module_names[0] == 'all':
        return modules, list(modules.keys())

    if context.branch.has_section("modules"):
        _included = []
        for (module_name, version) in context.branch.items(context.environment):
            version = str(version).lower().strip()

            if version == 'latest':
                _included.append(module_name)

            elif version == 'disable' or version == 'false' or version == '0' or version == '':
                continue
            else:
                spec = VersionSpec(version)
                mod = modules[module_name]

                if spec.match(mod.version_obj):
                    _included.append(module_name)
                else:
                    output.msgln("Ignoring " + mod + +" " + str(spec) + " does not match " + mod.version)

        return modules, _included

    return modules, []


def confirm(msg):
    if 'ARMORY_YES' in os.environ and os.environ['ARMORY_YES'] == 'YES':
        return True
    else:
        yesno = input(msg + ": (Y/n)? ")

        if yesno in ['y', 'Y', 'yes', '1']:
            return True
        else:
            return False
__author__ = 'kra869'

import subprocess
import hashlib
import os


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

    if context.branch.has_section(context.environment):
        _included = []
        _seen = []
        for (key, value) in context.branch.items(context.environment):
            val = str(value).lower().strip()
            if val == 'true':
                _included.append(key)

            _seen.append(key)

        for key in list(modules.keys()):

            if key in _seen:
                continue
            else:
                _included.append(key)

        return modules, _included
    else:
        return modules, list(modules.keys())


def confirm(msg):
    if 'ARMORY_YES' in os.environ and os.environ['ARMORY_YES'] == 'YES':
        return True
    else:
        yesno = input(msg + ": (yes/no)? ")

        if yesno in ['y', 'Y', 'yes', '1']:
            return True
        else:
            return False
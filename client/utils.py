__author__ = 'kra869'

import subprocess
import hashlib
import urlparse
import os

def register_scheme(scheme):
    for method in filter(lambda s: s.startswith('uses_'), dir(urlparse)):
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
    
def read_file(file):
    with open(file, 'r') as f:
        return f.read();
    
def build_modules (context, names=[], **kwargs):
    modules = context.modules.from_context(context)
    
    if len(names) == 0 or (len(names) == 1 and names[0] == 'all'):
        all = modules.keys()
    else:
        all = names

    
    if context.config.has_section(context.environment):
        included = []
        seen = []
        for (key, value) in context.config.items(context.environment):
            val = str(value).lower().strip()
            if val == 'true':
                included.append(key)
            else:
                print "Ignoring " + key + " in " + context.environment

            seen.append(key)

        for key in modules.keys():
            if key in seen:
                continue
            else:
                included.append(key)

        return (modules, included)
    else:
        return (modules, all)
        

def confirm(msg):
    if os.environ.has_key('ARMORY_YES') and os.environ['ARMORY_YES'] == 'YES':
        return True
    else:
        yesno = raw_input(msg+": (yes/no)? ")
        
        if yesno in ['y', 'Y', 'yes', '1']:
            return True
        else:
            return False
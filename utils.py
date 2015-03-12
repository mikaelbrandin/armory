__author__ = 'kra869'

import subprocess


def cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return out
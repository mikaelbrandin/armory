import sys


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    YELLOW = '\033[32m'
    LIGHT_RED = '\033[93m'
    RED = '\033[31m'
    END = '\033[0m'
    BOLD = '\033[1m'


def msgln(text, **kwargs):
    msg(text + "\n", **kwargs)


def msg(text, **kwargs):
    out = ""

    if 'label' in kwargs:
        if 'error' in kwargs:
            out += "[" + bcolors.RED + kwargs.get('label') + bcolors.END + "] "
        elif 'warn' in kwargs:
            out += "[" + bcolors.YELLOW + kwargs.get('label') + bcolors.END + "] "
        else:
            out += "[" + bcolors.GREEN + kwargs.get('label') + bcolors.END + "] "

    out += text
    sys.stdout.write(out)


def warn(text):
    print(bcolors.LIGHT_RED, text, bcolors.END)


def error(text):
    print(bcolors.RED, text, bcolors.END)


def ok(text=None):
    if text is None:
        print(bcolors.GREEN + "[ok]" + bcolors.END)
    else:
        print(bcolors.GREEN + "[ok]" + bcolors.END + text)
    

import sys
import os

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    LIGHT_RED = '\033[93m'
    RED = '\033[31m'
    END = '\033[0m'
    BOLD = '\033[1m'

def msgln(text):
    print(text)
    
def msg(text):
    sys.stdout.write(text)
    
def warn(text):
    print(bcolors.LIGHT_RED, text, bcolors.END)
    
def error(text):
    print(bcolors.RED, text, bcolors.END)
    
def ok(text=None):
    if text is None:
        print(bcolors.GREEN+"[ok]"+bcolors.END)
    else:
        print(bolcors.GREEN+"[ok]"+bcolors.END+text)
    
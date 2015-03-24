__author__ = 'kra869'

from . import base_client
import os
import getpass
import sys
import subprocess

class Client(base_client.IOClient):
    PUSH = "ssh {server} \"cd {path}; armory-push\""
    PULL = "ssh {server} \"cd {path}; armory-pull\""
    def __init__(self, uri):
        base_client.IOClient.__init__(self, uri)
      
        pass
        
    def connect(self, uri, feature):
        if feature is 'push':
            return self.get_shell(Client.PUSH)
        elif feature is 'pull':
            return self.get_shell(Client.PULL)
            
        return None
    
    def get_shell(self, cmd):
        cmd = cmd.format(server=self.uri.netloc, path=self.uri.path)
        shell = base_client.Shell(cmd, os.getcwd())
        self.check_askpass(shell)
        return shell
    
    def check_askpass(self, shell):
        while True:
            line = shell.read_line();
            if line.startswith('helo'):
                sys.stdout.write(line)
                return True;
            else:
                sys.stdout.write(line)
                pw = getpass.getpass();
                shell.write_line(pw)
        
    def cleanup(self):
        pass
        
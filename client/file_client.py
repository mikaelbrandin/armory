__author__ = 'kra869'

import base_client
import os
import getpass
import sys
import subprocess

class Client(base_client.IOClient):
    PUSH = "armory-push"
    PULL = "armory-pull"
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
        shell = base_client.Shell(cmd, self.uri.path)
        
        msg = shell.read_msg();
        if msg.msg == 'helo':
            return shell
        
        return None
        
    def cleanup(self):
        pass
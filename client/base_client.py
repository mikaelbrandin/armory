__author__ = 'mikael.brandin@devolver.se'

import os
import urlparse
import subprocess

class BaseClient:
    
    def push(self, package_name, pack_file, hash):
        pass;
        
    def pull(self):
        pass;

        
class IOClient(BaseClient):

    def __init__(self, uri):
        self.uri = urlparse.urlparse(uri)

    def connect(self, uri, feature):
        return None
        
    def cleanup(self):
        pass

    def push(self, package_name, pack_file, hash):
        shell = self.connect(self.uri, 'push')
        
        self.cleanup();
        pass;
        
    def pull(self):
        pass;
        

class Shell:
    def __init__(self, cmd, cwd):
        print "Call: "+cmd+" from "+cwd
        self.process = subprocess.Popen(cmd, shell=True, cwd=cwd, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read_msg(self):
        return proc.read_msg(self.process.stdout);
        
    def read_line(self):
        return self.process.stdout.readline();

    def write_msg(self, msg):
        return proc.write_msg(self.process.stdin, msg)

    def write_file(self, file, hash):
        return proc.write_file(self.process.stdin, file, hash)

    def read_file(self, file, hash):
        return proc.read_file(self.process.stdout, file, hash)

    def wait(self):
        self.process.wait();
__author__ = 'kra869'

import subprocess
import protocol as proc
import urlparse

class TimeoutException(BaseException):
    def __init__(self):
        pass
        

class Process:
    def __init__(self, cmd, cwd):
        self.process = subprocess.Popen([cmd], cwd=cwd, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
    def read_msg(self):
        return proc.read_msg(self.process.stdout);
            
    def write_msg(self, msg):
        return proc.write_msg(self.process.stdin, msg)
        
    def write_file(self,file, hash):
        return proc.write_file(self.process.stdin, file, hash)
        
    def read_file(self, package, hash):
        return proc.read_file(self.process.stdout, package, hash)
        
    def wait(self):
        self.process.wait();

class Client:
    def __init__(self, uri):
        self.uri = urlparse.urlparse(uri)
        pass
        
    def push(self, packageName, packageFile, packageHash):
          
        p = Process('armory-push', self.uri.path);
       
        msg = p.read_msg();
        p.write_msg("push {package} {hash}".format(package=packageName, hash=packageHash))
        p.write_msg("ok");
        
        msg = p.read_msg();
        
        if msg.msg == 'accept':
            print "accepted"
            p.write_file(packageFile, packageHash)
            p.wait()
            return None
        elif msg.msg == 'reject':
            print "rejected"
            return  None
        elif msg.msg == 'error':
            print "error"
            return  None
        else:
            print "oops"
            return None
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
        
    def read_file(self, file, hash):
        return proc.read_file(self.process.stdout, file, hash)
        
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
            print "-> "+packageName
            p.write_file(packageFile, packageHash)
            p.wait()
            return None
        elif msg.msg == 'reject':
            print "Rejected "+packageName
            return  None
        elif msg.msg == 'error':
            print "Error "+packageName
            return  None
        else:
            print "oops"
            return None
            
    def pull(self, module, version, dst):
        
        p = Process('armory-pull', self.uri.path);
        
        msg = p.read_msg();
        p.write_msg("pull /modules/"+module+'/'+version);
        p.write_msg("ok");
        
        msg = p.read_msg();
        if msg.msg == 'accept':
            p.read_file(dst, 0)
            p.wait()
            return None
        elif msg.msg == 'reject':
            print "Rejected"
            return  None
        elif msg.msg == 'error':
            print "Error "
            return  None
        else:
            print "oops"
            return None
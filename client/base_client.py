__author__ = 'mikael.brandin@devolver.se'

import os
import urlparse
import subprocess
import exceptions
import protocol

class ClientException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(ClientException, self).__init__(msg);

class BaseClient:
    
    def push(self, package_name, pack_file, hash):
        pass;
        
    def pull(self, module, version, dst):
        pass;
    
    def pull_branch(self, branch_name, home_directory):
        pass;

        
class IOClient(BaseClient):

    def __init__(self, uri):
        self.uri = urlparse.urlparse(uri)

    def connect(self, uri, feature):
        return None
        
    def cleanup(self):
        pass

    def push(self, package_name, pack_file, hash):
        
        if not os.path.exists(pack_file):
            raise ClientException("No such file: "+pack_file)
    
        shell = self.connect(self.uri, 'push')
        
        if shell is None:
            raise ClientException("unable to create shell");
        
        shell.write_msg("push {package} {hash}".format(package=package_name, hash=hash))
        shell.write_msg("ok");

        msg = shell.read_msg();

        if msg.msg == 'accept':
            print "accept: "+package_name
            shell.write_file(pack_file, hash)
            shell.wait()
            return None
        elif msg.msg == 'reject':
            print "reject: " + package_name
            return None
        elif msg.msg == 'error':
            print "error: " + package_name + " " + str(msg.params)
            return None
        else:
            print "unknown response: "+str(msg)
            return None
        
        
        self.cleanup();
        pass;
        
    def pull_branch(self, branch_name, home_directory):
        shell = self.connect(self.uri, 'pull')
        
        if shell is None:
            raise ClientException("unable to create shell");
                
        shell.write_msg("pull /branch/" + branch_name);
        shell.write_msg("ok");

        msg = shell.read_msg();
        if msg.msg == 'accept':
            shell.read_file(home_directory + branch_name, 0)
            shell.wait()
            return True
        elif msg.msg == 'reject':
            print "reject: "+module
            return False
        elif msg.msg == 'error':
            print "error: "+str(msg)
            return False
        else:
            print "unknown response: "+str(msg)
            return False
            
        return True
        
    def pull(self, module, version, dst):
        shell = self.connect(self.uri, 'pull')
        
        if shell is None:
            raise ClientException("unable to create shell");
                
        shell.write_msg("pull /modules/" + module + '/' + version);
        shell.write_msg("ok");

        msg = shell.read_msg();
        if msg.msg == 'accept':
            shell.read_file(dst, 0)
            shell.wait()
            return None
        elif msg.msg == 'reject':
            print "reject: "+module
            return None
        elif msg.msg == 'error':
            print "error: "+str(msg)
            return None
        else:
            print "unknown response: "+str(msg)
            return None
    
        pass;
        

class Shell:
    def __init__(self, cmd, cwd):
        self.process = subprocess.Popen(cmd, shell=True, cwd=cwd, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read_msg(self):
        return protocol.read_msg(self.process.stdout);
        
    def read_line(self):
        return self.process.stdout.readline();

    def write_msg(self, msg):
        return protocol.write_msg(self.process.stdin, msg)

    def write_file(self, file, hash):
        return protocol.write_file(self.process.stdin, file, hash)

    def read_file(self, file, hash):
        return protocol.read_file(self.process.stdout, file, hash)

    def wait(self):
        self.process.wait();
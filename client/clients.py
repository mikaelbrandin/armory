__author__ = 'kra869'

import ssh_client as ssh
import file_client as file

def create(uri):
    if uri.startswith('ssh://'):
        return ssh.Client(uri)
    elif uri.startswith('file://'):
        return file.Client(uri);
        


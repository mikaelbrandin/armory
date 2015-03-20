__author__ = 'kra869'

import file_client


class Client(file_client.Client):
    def __init__(self):
        super(Client, self)
        self.cmd = "ssh {username}@{host} cd {path}; armory-push".format(username=self.uri.username, host=self.uri.netloc, path=self.uri.path)
        pass
        
__author__ = 'kra869'

from . import base_client


class Client(base_client.IOClient):
    PUSH = "armory-push"
    PULL = "armory-pull"

    def __init__(self, uri):
        super(Client, self).__init__(uri)
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

        msg = shell.read_msg()
        if msg.msg == 'helo':
            return shell
        else:
            print("No helo: " + msg.msg)

        return None

    def cleanup(self):
        pass
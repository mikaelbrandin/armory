__author__ = 'kra869'


class ArmoryException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def print_message(self):
        print type(self).__name__ + ": " + self.msg

from . import exceptions
import os
import configparser
from . import output
import glob

class BranchException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(BranchException, self).__init__(msg)


def init(context):
    parser = context.register_command('branch', command_branch, aliases=['br'], help='Create, change and delete local branches')
    parser.add_argument('--set', '-s', metavar='BRANCH', help='switch to local branch BRANCH')
    parser.add_argument('--info', '-i', action='store_true', help='show information about branches')
 
    #parser.add_argument('repository', metavar='URI', help='repository to checkout from')
   
def command_branch(args, context):
    if args.set:
        move_to(context, args.set)
        output.msgln("Changed branch to "+args.set, label='ok')
    else:
        command_branch_info(args, context)

def command_branch_info(args, context):
    for branch_file in glob.iglob(context.home_directory + '*.armory'):
        name = os.path.basename(branch_file).split('.')[0]
        if name == context.branch_name:
            output.msgln(name, label='*')
        else:
            output.msgln(name, label=' ')

def move_to(context, branch):
    if not os.path.exists(context.home_directory+branch+'.armory'):
        raise BranchException("No branch "+branch+" in "+context.home_directory)

    if os.path.exists(context.db_directory + 'HEAD'):
        os.remove(context.db_directory + 'HEAD')
    
    os.symlink(context.home_directory + branch + '.armory', context.db_directory + 'HEAD')
    

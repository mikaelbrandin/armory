
import urllib.parse
from . import clients
import os
from . import clients
from . import exceptions
from . import output
from . import utils
from . import init as cmd_init
from .context import is_armory_repository_dir
from . import branch as cmd_branch
from . import output
import configparser

class CheckoutException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(CheckoutException, self).__init__(msg)


def init(context):
    parser = context.register_command('checkout', command_checkout, aliases=['co'], help='Checkout a repository branch to follow locally.')
    parser.add_argument('repository', metavar='BRANCH', help='repository to checkout from')
    
def command_checkout(args, context):

    #If we have a new remote repository don't just 
    #change to branch but pull down any changes.
    if '://' in args.repository:
        if not utils.confirm("Checkout "+args.repository+" to "+args.directory):
            return
            
        uri = urllib.parse.urlparse(args.repository)
        
        directory = os.path.dirname(uri.path)
        branch = os.path.basename(uri.path)    
        repository = uri.scheme + '://' + uri.netloc + directory + os.sep

        if branch.endswith('.armory'):
            branch = os.path.splitext(branch)[0]

        checkout(repository, branch, args.directory)
        cmd_branch.move_to(context, branch)
    else:
        #else just move to the new branch
        cmd_branch.move_to(context, args.repository)
    

def checkout(repository, branch, home_directory):

    if not is_armory_repository_dir(home_directory):
        output.msgln("Initalizing repository in "+home_directory)
        cmd_init.initialize(home_directory, repository)

    if os.path.exists(home_directory + branch + '.armory'):
        os.rename(home_directory + branch + '.armory', home_directory + branch + '.armory.bck')
    
    client = clients.create(repository)
    output.msgln("Pulling branch from "+repository)
    if not client.pull_branch(branch, home_directory):
        raise CheckoutException("unable to process branch: "+branch)
    output.msgln(branch, label='ok')
    
    
    #Read branch information
    #modules = context.modules.from_context(context)
    
    #Merge .branch with branch and save
    #Remove .branch
    #Pull non-existing modules
    #Upgrade for existing modules
    #Set current branch to branch in db/config


import urllib.parse
from . import clients
import os
from . import clients
from . import exceptions
from . import output
from . import init as cmd_init
from . import context as ctx

class CheckoutException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(CheckoutException, self).__init__(msg)


def init(context):
    parser = context.register_command('checkout', command_checkout, aliases=['co'], help='Checkout a repository branch to follow locally.')
    parser.add_argument('repository', metavar='URI', help='repository to checkout from')
    
def command_checkout(args, context):
    
    uri = urllib.parse.urlparse(args.repository)
    
    directory = os.path.dirname(uri.path)
    branch = os.path.basename(uri.path)    
    repository = uri.scheme + '://' + uri.netloc + directory
    
    if not ctx.is_armory_repository_dir(args.directory):
        print("Initalizing repository in "+args.directory)
        cmd_init.initialize(args.directory, repository)
    
    if branch.endswith('.armory'):
        branch = os.path.splitext(branch)[0]

    print("checkout "+branch+ " from "+repository)
    checkout(repository, branch, args.directory)
    
def checkout(repository, branch, home_directory):

    if os.path.exists(home_directory + branch + '.armory'):
        os.rename(home_directory + branch, context.home_directory + branch + '.old')
    
    client = clients.create(repository) 
    
    output.msgln(" reading "+branch+" to "+ home_directory)
    
    if not client.pull_branch(branch, home_directory):
        raise CheckoutException("unable to process branch: "+branch)
        
    #Read branch information
    #modules = context.modules.from_context(context)
    
    #Merge .branch with branch and save
    #Remove .branch
    #Pull non-existing modules
    #Upgrade for existing modules
    #Set current branch to branch in db/config

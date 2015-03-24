
import urllib.parse
from . import clients
import os
from . import clients
from . import exceptions

class CheckoutException(exceptions.ArmoryException):
    def __init__(self, msg):
        super(PushException, self).__init__(msg)


def init(context):
    parser = context.register_command('checkout', command_checkout, aliases=['co'], help='Checkout a repository branch to follow locally.')
    parser.add_argument('repository', metavar='URI', help='repository to checkout from')
    
def command_checkout(args, context):
    
    uri = urllib.parse.urlparse(args.repository)
    
    directory = os.path.dirname(uri.path)
    branch = os.path.basename(uri.path)    
    repository = uri.scheme + '://' + uri.netloc + directory

    print("checkout "+branch+ " from "+repository)
    checkout(repository, branch)
    
def checkout(repository, branch):
    
    if os.exists(context.home_directory + branch):
        os.rename(context.home_directory + branch, context.home_directory + '.' + branch)
    
    client = clients.create(repository) 
    
    if not client.pull_branch(branch, context.home_directory):
        raise CheckoutException("unable to process branch: "+branch)
        
    #Read branch information
    modules = context.modules.from_context(context)
    
    #Merge .branch with branch and save
    #Remove .branch
    #Pull non-existing modules
    #Upgrade for existing modules
    #Set current branch to branch in db/config

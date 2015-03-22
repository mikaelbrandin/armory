
def init(context):
    parser = context.register_command('checkout', command_checkout, help='Checkout a repository branch to follow locally.')
    parser.add_argument('repository', metavar='URI', nargs=1, help='repository to checkout from')
    parser.add_argument('--branch', metavar='BRANCH', help='Branch to checkout, default=main', default='main')
    

import sys
import os

def confirm(msg):
    if os.environ.has_key('ARMORY_YES') and os.environ['ARMORY_YES'] == 'YES':
        return True
    else:
        yesno = raw_input(msg+": (yes/no)? ")
        
        if yesno in ['y', 'Y', 'yes', '1']:
            return True
        else:
            return False
        
    
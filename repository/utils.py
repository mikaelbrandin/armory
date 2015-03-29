
import sys
import os

def confirm(msg):
    if 'ARMORY_YES' in os.environ and os.environ['ARMORY_YES'] == 'YES':
        return True
    else:
        yesno = input(msg+": (yes/no)? ")
        
        if yesno in ['y', 'Y', 'yes', '1']:
            return True
        else:
            return False
        
    
import os

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

armory_bin = os.path.dirname(os.path.realpath(__file__))

if os.path.exists('/usr/local/bin/armory'):
    os.remove('/usr/local/bin/armory')
    
if os.path.exists('/usr/local/bin/armory-push'):
    os.remove('/usr/local/bin/armory-push')
    
if os.path.exists('/usr/local/bin/army'):
    os.remove('/usr/local/bin/army')
    
if os.path.exists('/usr/local/bin/armory-pull'):
    os.remove('/usr/local/bin/armory-pull')

os.symlink(armory_bin + os.sep + "armory", "/usr/local/bin/armory")    
os.symlink(armory_bin + os.sep + "armory-push", "/usr/local/bin/armory-push")
os.symlink(armory_bin + os.sep + "army", "/usr/local/bin/army")
os.symlink(armory_bin + os.sep + "armory-pull", "/usr/local/bin/armory-pull")

import os

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

armory_bin = os.path.dirname(os.path.realpath(__file__))

os.symlink(armory_bin + os.sep + "armory", "/usr/local/bin/armory")

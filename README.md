# Armory
An deployment and management tool for Ubuntu/Linux

# Installation
Checkout code and run sudo python install.py

#Checkout local repository

    #Checkout a branch in the current context (directory)
    armory checkout <REPOSITORY>/<BRANCH>.armory

or

    #Initialize (create directory and checkout)
    armory init <REPOSITORY>/<BRANCH>.armory [DIR]

ex. armory init file:///opt/repository/

# Create modules
 
    armory module --create <NAME>

# Package and push changes

    armory package /module/directory/
    armory push <MODULE>.pack

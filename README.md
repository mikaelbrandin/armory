# Armory
An deployment and management tool for Ubuntu/Linux

# Installation
Checkout code and run sudo python install.py

#Checkout repository

    #Checkout a branch in the current context (directory)
    armory checkout <SCHEMA>://<REPOSITORY>/<BRANCH>.armory
    
#Switch to branch
    armory checkout <BRANCH>
    #or
    armory branch --set <BRANCH> 

#Create new repository from remote branch

    #Initialize (create directory and checkout)
    armory init <REPOSITORY>/<BRANCH>.armory [DIR]

ex. armory init file:///opt/repository/

# Create modules
 
    armory module --create <NAME>

# Package and Push changes
    
    # Package a module of configuration directory (to current directory)
    armory package /module/directory/
    
    # Push package to default remote repostory
    armory push <MODULE>.pack
    # or
    armory push --repository ssh://armory@myserver/opt/repository <MODULE>.pack

# Update modules and configuration

    # Update all packages in current (HEAD) branch.
    # -u|--update means that you will update/check existing modules and configurations.
    # Without -u only missing modules and configurations are downloaded.
    armory pull -u
    
# Full upgrade
    # Update branch informatin
    armory checkout ssh://armory@myserver/opt/repository/production.armory
    # Update and overwrite modules and configurations aligned to branch
    armory pull ---update
    # Clean up (remove unused versions of modules and configurations)
    armory clean --modules --configurations

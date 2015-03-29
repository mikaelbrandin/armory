# Armory
An deployment and management tool for Ubuntu/Linux

Armory provides a toolset for maintaining the life cycle of packges of binaries (modules) and configurations for binaries in branch. A branch is a running configuration traditionally mapping to development, production and staging like operations.

Armory supports a more flexible approche to working with branches of configuration and how to distribute configurations to several nodes in your deployment.

Considering a normal case of a development environment running many nodes in a local fashion and a production branch operating over several hosts and machines Armory provides a toolset for packaging and distributing this to said machines and
host much like version control systems like Git operate.

# Installation
Checkout code and run sudo python install.py

# Getting Started

## Checkout repository

    #Checkout a branch in the current context (directory)
    armory checkout <SCHEMA>://<REPOSITORY>/<BRANCH>.armory

## Pull modules in branch

    armory pull
    
## Start a module

    armory start <MODULE>
    
## Start all modules in branch

    armory start
    
## Stop a module
    
    armory stop <MODULE

## Stop all modules in branch

    armory stop
    
## Switch to branch

    armory checkout <BRANCH>
    #or
    armory branch --set <BRANCH> 

## Create new repository from remote branch

    #Initialize (create directory and checkout)
    armory init <REPOSITORY>/<BRANCH>.armory [DIR]

ex. armory init file:///opt/repository/

## Create modules
 
    armory module --create <NAME>

## Package and Push changes
    
    # Package a module of configuration directory (to current directory)
    armory package /module/directory/
    
    # Push package to default remote repostory
    armory push <MODULE>.pack
    # or
    armory push --repository ssh://armory@myserver/opt/repository <MODULE>.pack

## Update modules and configuration

    # Update all packages in current (HEAD) branch.
    # -u|--update means that you will update/check existing modules and configurations.
    # Without -u only missing modules and configurations are downloaded.
    armory pull -u
    
## Full upgrade
    # Update branch informatin
    armory checkout ssh://armory@myserver/opt/repository/production.armory
    # Update and overwrite modules and configurations aligned to branch
    armory pull ---update
    # Clean up (remove unused versions of modules and configurations)
    armory clean --modules --configurations

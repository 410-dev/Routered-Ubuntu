from modules.envchk import isRunningSudo, getOSDistribution, getOSBaseDistribution
import os

def check(hasForce: bool = False):
    # Check if the script is running in linux ubuntu
    # If based on linux debian, this script will still work.
    #   Therefore, if argument has --force, then the script will still run if the OS is debian based distro.
    #   If the argument does not have --force, then the script will exit.
    # If not based on linux debian, this script will not work anyway.
    
    # Check arguments if --force is present
    if hasForce:
        if getOSBaseDistribution() != "debian":
            print("The force argument is only supported in Debian based Linux. Your identified OS is " + getOSBaseDistribution() + " which is not supported.")
            exit(1)
    
    if getOSDistribution() != "linux.ubuntu":
        print("This script is only supported in Linux Ubuntu. Your identified OS is " + getOSDistribution() + " which is not supported.")
        exit(1)
        
    # Check if the script is running as root
    if not isRunningSudo():
        print("This script must be run as root")
        exit(1)
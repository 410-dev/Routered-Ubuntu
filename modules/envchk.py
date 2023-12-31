import platform
import os

import modules.fio as file

def getOSDistribution():
    system = platform.system()
    if system == 'Linux':
        if os.path.exists("/etc/os-release"):
            content = file.read("/etc/os-release")
            for line in content.split("\n"):
                if line.startswith("ID="):
                    return "linux." + line.split("=")[1].lower()
            return "linux.unidentified"
        elif os.path.exists("/etc/debian_version"):
            return "linux.debian"
        elif os.path.exists("/etc/redhat-release"):
            return "linux.redhat"
        else:
            return "linux.unknown"
    elif system == 'Darwin':
        return "darwin.macOS"
    elif system == 'Windows':
        return "nt.Windows"
    else:
        return ""
    
def getOSBaseDistribution():
    distro = getOSDistribution()
    if distro.startswith("linux."):
        if os.path.exists("/etc/debian_version"):
            return "debian"
        elif os.path.exists("/etc/redhat-release"):
            return "redhat"
        elif os.path.exists("/etc/os-release"):
            content = file.read("/etc/os-release")
            for line in content.split("\n"):
                if line.startswith("ID_LIKE="):
                    return line.split("=")[1]
            for line in content.split("\n"):
                if line.startswith("ID="):
                    return line.split("=")[1]
            return "linux"
        else:
            return "linux"
    else:
        return distro.split(".")[0]
        
def isRunningSudo():
    return os.geteuid() == 0

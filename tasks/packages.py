from modules.executor import exec, args
from modules.ui import menu

def check():
    
    # Try installing dialog if not installed.
    # If it fails, exit.
    output = exec(args("which dialog"))[1]
    if output == '' or output == None or output == '\n' or not output.startswith('/'):
        print("Installing dialog...")
        exit_c: tuple = exec(args("sudo apt install -y dialog"))
        if exit_c[0] != 0:
            print(f"Failed to install dialog: {exit_c[2]}")
            exit(1)
        print("dialog installed!")
    
    while(True):
        # List of packages required
        required = [
            "isc-dhcp-server",
            "net-tools",
            "hostapd",
        ]
            
        # Check if all required packages are installed
        missing = []
        for package in required:
            execResult = exec(args(f"dpkg -s {package}"))
            if execResult[0] != 0:
                missing.append(package)
                
        
        # If there are missing packages, ask and install
        if len(missing) == 0:
            print("All required packages are installed :)")
            return
        
        options: list = ["Install all missing packages"]
        
        for package in missing:
            options.append(f"Install {package}")
            
        options.append("Exit")
        
        selected: int = menu(options)
        
        if selected == 0:
            print("Installing all missing packages...")
            exitc = exec(args(f"sudo apt install -y {' '.join(missing)}"))
            if exitc[0] != 0:
                print(f"Failed to install all missing packages: {exitc[2]}")
                continue
            return True
        
        elif selected == len(options) - 1:
            print("Exiting...")
            exit(0)
        
        else:
            print(f"Installing {missing[selected - 1]}...")
            exec(args(f"sudo apt install -y {missing[selected - 1]}"))
            print(f"{missing[selected - 1]} installed!")
        
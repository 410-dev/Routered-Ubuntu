import modules.devices as devices
import modules.ui as ui
import modules.fio as file
from modules.executor import exec, args

def run():
    netinterfaces: list = devices.networkInterfaces(False)
    
    # Run ifconfig
    results: list = []
    for interface in netinterfaces:
        result = exec(args(f"ifconfig {interface}"))[1]
        if "error fetching interface information" in result.lower():
            continue
        results.append(result)
        
    # High priority if it has an ip address: detect inet keyword
    netinterfaces: list = []
    for result in results:
        # Get the interface name
        interface = result.split(":")[0]
        netinterfaces.append((interface, result, "inet" in result))
        
    # Sort by IP assigned
    netinterfaces.sort(key=lambda x: x[2], reverse=True)
        
    options: list = []
    for interface in netinterfaces:
        options.append(f"{interface[0]}: {'(IP Assigned)' if interface[2] else '(IP Not assigned)'}")
        
    options.append("Exit")
        
    selected: int = ui.menu(options, height=20, title="Select WAN (Internet) Interface")
    if selected == len(options) - 1:
        return
    file.write("data/wan.interface", netinterfaces[selected][0])
    ui.msgBox(f"Selected WAN interface: {netinterfaces[selected][0]}", "Setting Queue")
    print(f"Selected WAN interface: {netinterfaces[selected][0]}")
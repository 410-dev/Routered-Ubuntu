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
        
    # Sort by IP unassigned
    netinterfaces.sort(key=lambda x: x[2], reverse=False)    
    
    options: list = []
    for interface in netinterfaces:
        options.append(f"{interface[0]}: {'(IP Assigned)' if interface[2] else '(IP Not assigned)'}")
        
    options.append("Exit")
        
    selected: int = ui.menu(options, height=20, title="Select Interface to assign IP to")
    if selected == len(options) - 1:
        return
    
    ipAddr: str = ui.read("Enter IP Address to assign to interface", default=f"{file.read('data/dhcp.option_routers') if file.exists('data/dhcp.option_routers') else ''}")
    ipAddr.strip()
    if ipAddr == "":
        return
    
    yn: bool = ui.yesno(f"Are you sure you want to assign {ipAddr} to {netinterfaces[selected][0]}? This will be applied immediately.", "Confirm IP Assignment")
    
    if not yn:
        return
    
    output = exec(args(f"sudo ip addr add {ipAddr}/24 dev {netinterfaces[selected][0]}"))
    
    if output[0] != 0:
        ui.msgBox(f"Error assigning IP address to interface {netinterfaces[selected][0]}.", "Error")
        return
    
    ui.msgBox(f"IP address {ipAddr} assigned to interface {netinterfaces[selected][0]}.", "Setting Updated")
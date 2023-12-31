import modules.ui as ui
import modules.fio as file

from tasks.apply import getKeys

def run():
    yesno: bool = ui.yesno("This will destroy unsaved data. Continue?", "Unsaved Configuration Destruction Alert")
    if not yesno: return
    
    # Read file /etc/dhcp/dhcpd.conf
    # Read file /etc/default/isc-dhcp-server
    # Read file /etc/hostapd/hostapd.conf
    
    dhcpdconf: str = file.read("/etc/dhcp/dhcpd.conf")
    dhcpdconf: list = dhcpdconf.split("\n")
    dhcpdconf: list = [line for line in dhcpdconf if not line.startswith("#") and not line.startswith(";") and not line.startswith("//")]
    
    iscdhcpserver: str = file.read("/etc/default/isc-dhcp-server")
    iscdhcpserver: list = iscdhcpserver.split("\n")
    iscdhcpserver: list = [line for line in iscdhcpserver if not line.startswith("#") and not line.startswith(";") and not line.startswith("//")]
    
    hostapdconf: str = file.read("/etc/hostapd/hostapd.conf")
    hostapdconf: list = hostapdconf.split("\n")
    hostapdconf: list = [line for line in hostapdconf if not line.startswith("#") and not line.startswith(";") and not line.startswith("//")]
    
    keys: list = getKeys()
    
    # Parse values from hostapd.conf
    for line in hostapdconf:
        for key in keys:
            akey = key.split(".")[1]
            if line.startswith(akey + "="):
                file.write(f"data/{key}", line.split("=")[1])
    
    # Parse values from dhcpd.conf
    for line in dhcpdconf:
        line = line.strip()
        if line.startswith("default-lease-time"):
            file.write("data/dhcp.default_lease_time", line.split(" ")[1].replace(";", ""))
            
        elif line.startswith("max-lease-time"):
            file.write("data/dhcp.max_lease_time", line.split(" ")[1].replace(";", ""))
            
        elif line.startswith("subnet"):
            file.write("data/dhcp.subnet_ip", line.split(" ")[1].replace(";", ""))
            file.write("data/dhcp.netmask", line.split(" ")[3].replace(";", ""))
            
        elif line.startswith("option routers"):
            file.write("data/dhcp.option_routers", line.split(" ")[2].replace(";", ""))
            
        elif line.startswith("option domain-name-servers"):
            file.write("data/dhcp.option_domain_name_servers", ' '.join(line.split(" ")[2:]).replace(";", ""))
            
        elif line.startswith("option broadcast-address"):
            file.write("data/dhcp.option_broadcast_address", line.split(" ")[2].replace(";", ""))
            
        elif line.startswith("range"):
            file.write("data/dhcp.range_start", line.split(" ")[1])
            file.write("data/dhcp.range_end", line.split(" ")[2].replace(";", ""))
            
        elif line.startswith("authoritative"):
            file.write("data/dhcp.authoritative", "1")
            
    # Parse values from iscdhcpserver
    for line in iscdhcpserver:
        if line.startswith("INTERFACES"):
            file.write("data/dhcp.interface", line.split("=")[1])
            
    ui.msgBox("Parsed values from existing values.", "Success")
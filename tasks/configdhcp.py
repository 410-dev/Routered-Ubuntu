import modules.ui as ui
import modules.fio as file

def load(key: str, default: str ) -> str:
    if not file.exists(f"data/dhcp.{key}"):
        save(key, default)
        return default
    return file.read(f"data/dhcp.{key}")

def loadNoDefault(key: str) -> str:
    if not file.exists(f"data/dhcp.{key}"):
        if key.endswith("tmp"):
            if file.exists(f"data/dhcp.{key[:-4]}"):
                return file.read(f"data/dhcp.{key[:-4]}")
        return ""
    return file.read(f"data/dhcp.{key}")

def save(key: str, value: str) -> None:
    file.write(f"data/dhcp.{key}", value)


def run():
    while True:
        default_lease_time: str = load("default_lease_time", "600")
        max_lease_time: str = load("max_lease_time", "7200")
        subnet_ip: str = load("subnet_ip", "192.168.1.0")
        netmask: str = load("netmask", "255.255.255.0")
        authoritative: str = load("authoritative", "1")
        range_start: str = load("range_start", "192.168.1.150")
        range_end: str = load("range_end", "192.168.1.255")
        option_routers: str = load("option_routers", "192.168.1.1")
        option_domain_name_servers: str = load("option_domain_name_servers", "8.8.8.8, 8.8.4.4")
        option_broadcast_address: str = load("option_broadcast_address", "192.168.1.255")
        
        # if temporary exists, load it
        if file.exists("data/dhcp.default_lease_time.tmp"):
            default_lease_time = loadNoDefault("default_lease_time.tmp")
        if file.exists("data/dhcp.max_lease_time.tmp"):
            max_lease_time = loadNoDefault("max_lease_time.tmp")
        if file.exists("data/dhcp.subnet_ip.tmp"):
            subnet_ip = loadNoDefault("subnet_ip.tmp")
        if file.exists("data/dhcp.netmask.tmp"):
            netmask = loadNoDefault("netmask.tmp")
        if file.exists("data/dhcp.authoritative.tmp"):
            authoritative = loadNoDefault("authoritative.tmp")
        if file.exists("data/dhcp.range_start.tmp"):
            range_start = loadNoDefault("range_start.tmp")
        if file.exists("data/dhcp.range_end.tmp"):
            range_end = loadNoDefault("range_end.tmp")
        if file.exists("data/dhcp.option_routers.tmp"):
            option_routers = loadNoDefault("option_routers.tmp")
        if file.exists("data/dhcp.option_domain_name_servers.tmp"):
            option_domain_name_servers = loadNoDefault("option_domain_name_servers.tmp")
        if file.exists("data/dhcp.option_broadcast_address.tmp"):
            option_broadcast_address = loadNoDefault("option_broadcast_address.tmp")
        
        options: list = [
            f"Default Lease Time          Current: {default_lease_time}",
            f"Max Lease Time              Current: {max_lease_time}",
            f"Subnet IP                   Current: {subnet_ip}",
            f"Netmask                     Current: {netmask}",
            f"Authoritative               Current: {authoritative}",
            f"Range Start                 Current: {range_start}",
            f"Range End                   Current: {range_end}",
            f"Option Routers              Current: {option_routers}",
            f"Option Domain Name Servers  Current: {option_domain_name_servers}",
            f"Option Broadcast Address    Current: {option_broadcast_address}",
            "Save and exit",
            "Exit without saving"
        ]
        
        selection: int = ui.menu(options, "DHCP Settings", height=30)
        
        if selection == 0:
            default_lease_time = ui.read("Default Lease Time", default_lease_time)
            save("default_lease_time.tmp", default_lease_time)
            
        elif selection == 1:
            max_lease_time = ui.read("Max Lease Time", max_lease_time)
            save("max_lease_time.tmp", max_lease_time)
            
        elif selection == 2:
            subnet_ip = ui.read("Subnet IP", subnet_ip)
            save("subnet_ip.tmp", subnet_ip)
            
        elif selection == 3:
            netmask = ui.read("Netmask", netmask)
            save("netmask.tmp", netmask)
            
        elif selection == 4:
            authoritative = ui.read("Authoritative", authoritative)
            save("authoritative.tmp", authoritative)
            
        elif selection == 5:
            range_start = ui.read("Range Start", range_start)
            save("range_start.tmp", range_start)
            
        elif selection == 6:
            range_end = ui.read("Range End", range_end)
            save("range_end.tmp", range_end)
            
        elif selection == 7:
            option_routers = ui.read("Option Routers", option_routers)
            save("option_routers.tmp", option_routers)
            
        elif selection == 8:
            option_domain_name_servers = ui.read("Option Domain Name Servers", option_domain_name_servers)
            save("option_domain_name_servers.tmp", option_domain_name_servers)
            
        elif selection == 9:
            option_broadcast_address = ui.read("Option Broadcast Address", option_broadcast_address)
            save("option_broadcast_address.tmp", option_broadcast_address)
            
        elif selection == 10:
            savePermanently()
            remove()
            break
        
        else:
            print("Exiting...")
            remove()
            return
        
def savePermanently(): 
    save("default_lease_time", loadNoDefault("default_lease_time.tmp"))
    save("max_lease_time", loadNoDefault("max_lease_time.tmp"))
    save("subnet_ip", loadNoDefault("subnet_ip.tmp"))
    save("netmask", loadNoDefault("netmask.tmp"))
    save("authoritative", loadNoDefault("authoritative.tmp"))
    save("range_start", loadNoDefault("range_start.tmp"))
    save("range_end", loadNoDefault("range_end.tmp"))
    save("option_routers", loadNoDefault("option_routers.tmp"))
    save("option_domain_name_servers", loadNoDefault("option_domain_name_servers.tmp"))
    save("option_broadcast_address", loadNoDefault("option_broadcast_address.tmp"))
    ui.msgBox("Configuration updated.", "Setting Queue")

    
def remove():
    file.remove("data/dhcp.default_lease_time.tmp")
    file.remove("data/dhcp.max_lease_time.tmp")
    file.remove("data/dhcp.subnet_ip.tmp")
    file.remove("data/dhcp.netmask.tmp")
    file.remove("data/dhcp.authoritative.tmp")
    file.remove("data/dhcp.range_start.tmp")
    file.remove("data/dhcp.range_end.tmp")
    file.remove("data/dhcp.option_routers.tmp")
    file.remove("data/dhcp.option_domain_name_servers.tmp")
    file.remove("data/dhcp.option_broadcast_address.tmp")
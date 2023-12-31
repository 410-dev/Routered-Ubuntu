import datetime
import modules.fio as file
import modules.ui as ui

import os

def getKeys() -> list:
    keys: list = [
        "wan.interface",
        "wifi.interface",
        "wifi.ssid",
        "wifi.wpa_passphrase",
        "wifi.driver",
        "wifi.hw_mode",
        "wifi.channel",
        "wifi.wmm_enabled",
        "wifi.macaddr_acl",
        "wifi.auth_algs",
        "wifi.ignore_broadcast_ssid",
        "wifi.wpa",
        "wifi.wpa_key_mgmt",
        "wifi.wpa_pairwise",
        "wifi.rsn_pairwise",
        "dhcp.default_lease_time",
        "dhcp.max_lease_time",
        "dhcp.subnet_ip",
        "dhcp.netmask",
        "dhcp.authoritative",
        "dhcp.range_start",
        "dhcp.range_end",
        "dhcp.option_routers",
        "dhcp.option_domain_name_servers",
        "dhcp.option_broadcast_address"
    ]
    return keys

def loadAllKeys() -> dict:
    settings: dict = {}
    
    for key in getKeys():
        settings[key] = file.read(f"data/{key}")
        
    return settings

def getMissingKeys() -> list:
    missing: list = []
    
    for key in getKeys():
        if not file.exists(f"data/{key}"):
            missing.append(key)
            
    return missing

def run():
    # Check if all keys are present
    missingKeys: list = getMissingKeys()
    
    if len(missingKeys) > 0:
        ui.msgBox(f"Missing keys: {', '.join(missingKeys)}", "Error")
        return
    
    # Load all keys
    keys: dict = loadAllKeys()
    
    # Ask for correct
    keyStr: str = ""
    for key in keys:
        keyStr += f"{key}={keys[key]}\n"
        
    correct: bool = ui.yesno(f"Are these settings correct?\n{keyStr}", "Confirm", height=40, width=65)
    if not correct:
        return
    
    # Apply settings
    # /etc/dhcp/dhcpd.conf
    print(f"Applying settings to /etc/dhcp/dhcpd.conf")
    if os.path.exists("/etc/dhcp/dhcpd.conf"):
        currentDate = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f"Existing dhcpd.conf found, backing up to dhcpd.conf.bak.{currentDate}")
        os.rename("/etc/dhcp/dhcpd.conf", f"/etc/dhcp/dhcpd.conf.bak.{currentDate}")
        
    dhcpdConf: str = f"""\
default-lease-time {keys['dhcp.default_lease_time']};
max-lease-time {keys['dhcp.max_lease_time']};

subnet {keys['dhcp.subnet_ip']} netmask {keys['dhcp.netmask']} {{
    interface {keys['wifi.interface']};
    { 'authoritative;' if keys['dhcp.authoritative'] == '1' else ''}
    option routers {keys['dhcp.option_routers']};
    option domain-name-servers {keys['dhcp.option_domain_name_servers']};
    option broadcast-address {keys['dhcp.option_broadcast_address']};
    range {keys['dhcp.range_start']} {keys['dhcp.range_end']};
}}
"""
    file.write("/etc/dhcp/dhcpd.conf", dhcpdConf)
    
    # /etc/default/isc-dhcp-server
    print(f"Applying settings to /etc/default/isc-dhcp-server")
    if os.path.exists("/etc/default/isc-dhcp-server"):
        currentDate = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f"Existing isc-dhcp-server found, backing up to isc-dhcp-server.bak.{currentDate}")
        os.rename("/etc/default/isc-dhcp-server", f"/etc/default/isc-dhcp-server.bak.{currentDate}")
        
    iscDhcpServer: str = f"""\
INTERFACESv4="{keys['wifi.interface']}"
INTERFACES="{keys['wifi.interface']}"
"""
    file.write("/etc/default/isc-dhcp-server", iscDhcpServer)
    
    # /etc/netplan/01-netcfg.yaml
    print(f"Applying settings to /etc/netplan/01-netcfg.yaml")
    if os.path.exists("/etc/netplan/01-netcfg.yaml"):
        currentDate = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f"Existing 01-netcfg.yaml found, backing up to 01-netcfg.yaml.bak.{currentDate}")
        os.rename("/etc/netplan/01-netcfg.yaml", f"/etc/netplan/01-netcfg.yaml.bak.{currentDate}")
        
    netplan: str = f"""\
network:
    version: 2
    renderer: networkd
    ethernets:
        {keys['wan.interface']}:
            dhcp4: true
            addresses: [{keys['dhcp.subnet_ip']}/{keys['dhcp.netmask']}]
    
    wifis:
        {keys['wifi.interface']}:
            addresses: [{keys['dhcp.subnet_ip']}/{keys['dhcp.netmask']}]
            access-points:
                "{keys['wifi.ssid']}":
                    password: "{keys['wifi.wpa_passphrase']}"                 
"""
    file.write("/etc/netplan/01-netcfg.yaml", netplan)
    
    # /etc/hostapd/hostapd.conf
    print(f"Applying settings to /etc/hostapd/hostapd.conf")
    if os.path.exists("/etc/hostapd/hostapd.conf"):
        currentDate = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f"Existing hostapd.conf found, backing up to hostapd.conf.bak.{currentDate}")
        os.rename("/etc/hostapd/hostapd.conf", f"/etc/hostapd/hostapd.conf.bak.{currentDate}")
        
    hostapd: str = f"""\
interface={keys['wifi.interface']}
driver={keys['wifi.driver']}
ssid={keys['wifi.ssid']}
hw_mode={keys['wifi.hw_mode']}
channel={keys['wifi.channel']}
wmm_enabled={keys['wifi.wmm_enabled']}
macaddr_acl={keys['wifi.macaddr_acl']}
auth_algs={keys['wifi.auth_algs']}
ignore_broadcast_ssid={keys['wifi.ignore_broadcast_ssid']}
wpa={keys['wifi.wpa']}
wpa_key_mgmt={keys['wifi.wpa_key_mgmt']}
wpa_pairwise={keys['wifi.wpa_pairwise']}
rsn_pairwise={keys['wifi.rsn_pairwise']}
wpa_passphrase={keys['wifi.wpa_passphrase']}
"""
    file.write("/etc/hostapd/hostapd.conf", hostapd)
    
    print(f"Enabling IPV4 forwarding in /etc/sysctl.conf")
    sysctl: str = file.read("/etc/sysctl.conf")
    if not "net.ipv4.ip_forward=1" in sysctl:
        sysctl += "net.ipv4.ip_forward=1\n"
        file.write("/etc/sysctl.conf", sysctl)
    else:
        print("IPV4 forwarding already enabled")
    
    # Done
    ui.msgBox("Settings applied successfully", "Success")
    
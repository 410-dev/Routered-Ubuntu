import modules.devices as devices
import modules.ui as ui
import modules.fio as file
from modules.executor import exec, args

def load(key: str, default: str ) -> str:
    if not file.exists(f"data/wifi.{key}"):
        save(key, default)
        return default
    return file.read(f"data/wifi.{key}")

def loadNoDefault(key: str) -> str:
    if not file.exists(f"data/wifi.{key}"):
        if key.endswith("tmp"):
            if file.exists(f"data/wifi.{key[:-4]}"):
                return file.read(f"data/wifi.{key[:-4]}")
        return ""
    return file.read(f"data/wifi.{key}")

def save(key: str, value: str) -> None:
    file.write(f"data/wifi.{key}", value)

def run():
    
    while True:
        ssid: str = load("ssid", "")
        wpa_passphrase: str = load("wpa_passphrase", "")
        driver: str = load("driver", "nl80211")
        hw_mode: str = load("hw_mode", "g")
        channel: str = load("channel", "7")
        wmm_enabled: str = load("wmm_enabled", "0")
        macaddr_acl: str = load("macaddr_acl", "0")
        auth_algs: str = load("auth_algs", "1")
        ignore_broadcast_ssid: str = load("ignore_broadcast_ssid", "0")
        wpa: str = load("wpa", "2")
        wpa_key_mgmt: str = load("wpa_key_mgmt", "WPA-PSK")
        wpa_pairwise: str = load("wpa_pairwise", "TKIP")
        rsn_pairwise: str = load("rsn_pairwise", "CCMP")
        
        if file.exists("data/wifi.ssid.tmp"):
            ssid = loadNoDefault("ssid.tmp")
        if file.exists("data/wifi.wpa_passphrase.tmp"):
            wpa_passphrase = loadNoDefault("wpa_passphrase.tmp")
        if file.exists("data/wifi.driver.tmp"):
            driver = loadNoDefault("driver.tmp")
        if file.exists("data/wifi.hw_mode.tmp"):
            hw_mode = loadNoDefault("hw_mode.tmp")
        if file.exists("data/wifi.channel.tmp"):
            channel = loadNoDefault("channel.tmp")
        if file.exists("data/wifi.wmm_enabled.tmp"):
            wmm_enabled = loadNoDefault("wmm_enabled.tmp")
        if file.exists("data/wifi.macaddr_acl.tmp"):
            macaddr_acl = loadNoDefault("macaddr_acl.tmp")
        if file.exists("data/wifi.auth_algs.tmp"):
            auth_algs = loadNoDefault("auth_algs.tmp")
        if file.exists("data/wifi.ignore_broadcast_ssid.tmp"):
            ignore_broadcast_ssid = loadNoDefault("ignore_broadcast_ssid.tmp")
        if file.exists("data/wifi.wpa.tmp"):
            wpa = loadNoDefault("wpa.tmp")
        if file.exists("data/wifi.wpa_key_mgmt.tmp"):
            wpa_key_mgmt = loadNoDefault("wpa_key_mgmt.tmp")
        if file.exists("data/wifi.wpa_pairwise.tmp"):
            wpa_pairwise = loadNoDefault("wpa_pairwise.tmp")
        if file.exists("data/wifi.rsn_pairwise.tmp"):
            rsn_pairwise = loadNoDefault("rsn_pairwise.tmp")
        
        options: list = [
            f"WiFi SSID (WiFi Name)       Current: {ssid}",
            f"WiFi Password               Current: {wpa_passphrase}",
            f"WiFi Driver                 Current: {driver}",
            f"WiFi Mode                   Current: {hw_mode}",
            f"WiFi Channel                Current: {channel}",
            f"WiFi WMM Enabled            Current: {wmm_enabled}",
            f"WiFi MAC ACL                Current: {macaddr_acl}",
            f"WiFi Auth Algs              Current: {auth_algs}",
            f"WiFi Ignore Broadcast SSID  Current: {ignore_broadcast_ssid}",
            f"WiFi WPA                    Current: {wpa}",
            f"WiFi WPA Key MGMT           Current: {wpa_key_mgmt}",
            f"WiFi WPA Pairwise           Current: {wpa_pairwise}",    
            f"WiFi RSN Pairwise           Current: {rsn_pairwise}",
            "Save and exit",
            "Exit without saving"
        ]
        
        selection: int = ui.menu(options, "WiFi Settings", height=40)
        
        if selection == 0:
            ssid = ui.read("SSID (WiFi Name)", ssid)
            save("ssid.tmp", ssid)
            
        elif selection == 1:
            wpa_passphrase = ui.read("Password", wpa_passphrase)
            save("wpa_passphrase.tmp", wpa_passphrase)
            
        elif selection == 2:
            driver = ui.read("Driver", driver)
            save("driver.tmp", driver)
            
        elif selection == 3:
            hw_mode = ui.read("Mode", hw_mode)
            save("hw_mode.tmp", hw_mode)
            
        elif selection == 4:
            channel = ui.read("Channel", channel)
            save("channel.tmp", channel)
            
        elif selection == 5:
            wmm_enabled = ui.read("WMM Enabled", wmm_enabled)
            save("wmm_enabled.tmp", wmm_enabled)
            
        elif selection == 6:
            macaddr_acl = ui.read("MAC ACL", macaddr_acl)
            save("macaddr_acl.tmp", macaddr_acl)
            
        elif selection == 7:
            auth_algs = ui.read("Auth Algs", auth_algs)
            save("auth_algs.tmp", auth_algs)
            
        elif selection == 8:
            ignore_broadcast_ssid = ui.read("Ignore Broadcast SSID", ignore_broadcast_ssid)
            save("ignore_broadcast_ssid.tmp", ignore_broadcast_ssid)
            
        elif selection == 9:
            wpa = ui.read("WPA", wpa)
            save("wpa.tmp", wpa)
            
        elif selection == 10:
            wpa_key_mgmt = ui.read("WPA Key MGMT", wpa_key_mgmt)
            save("wpa_key_mgmt.tmp", wpa_key_mgmt)
            
        elif selection == 11:
            wpa_pairwise = ui.read("WPA Pairwise", wpa_pairwise)
            save("wpa_pairwise.tmp", wpa_pairwise)
            
        elif selection == 12:
            rsn_pairwise = ui.read("RSN Pairwise", rsn_pairwise)
            save("rsn_pairwise.tmp", rsn_pairwise)
            
        elif selection == 13:
            print("Saving and exiting...")
            savePermanently()
            remove()
            break
        
        elif selection == 14:
            remove()
            print("Exiting...")
            return
            
        else:
            print("Invalid option!")
            continue
    

def savePermanently():
    save("ssid", loadNoDefault("ssid.tmp"))
    save("wpa_passphrase", loadNoDefault("wpa_passphrase.tmp"))
    save("driver", loadNoDefault("driver.tmp"))
    save("hw_mode", loadNoDefault("hw_mode.tmp"))
    save("channel", loadNoDefault("channel.tmp"))
    save("wmm_enabled", loadNoDefault("wmm_enabled.tmp"))
    save("macaddr_acl", loadNoDefault("macaddr_acl.tmp"))
    save("auth_algs", loadNoDefault("auth_algs.tmp"))
    save("ignore_broadcast_ssid", loadNoDefault("ignore_broadcast_ssid.tmp"))
    save("wpa", loadNoDefault("wpa.tmp"))
    save("wpa_key_mgmt", loadNoDefault("wpa_key_mgmt.tmp"))
    save("wpa_pairwise", loadNoDefault("wpa_pairwise.tmp"))
    save("rsn_pairwise", loadNoDefault("rsn_pairwise.tmp"))
    ui.msgBox("Configuration updated.", "Setting Queue")

def remove():
    # Remove temporary files
    file.remove("data/wifi.ssid.tmp")
    file.remove("data/wifi.wpa_passphrase.tmp")
    file.remove("data/wifi.driver.tmp")
    file.remove("data/wifi.hw_mode.tmp")
    file.remove("data/wifi.channel.tmp")
    file.remove("data/wifi.wmm_enabled.tmp")
    file.remove("data/wifi.macaddr_acl.tmp")
    file.remove("data/wifi.auth_algs.tmp")
    file.remove("data/wifi.ignore_broadcast_ssid.tmp")
    file.remove("data/wifi.wpa.tmp")
    file.remove("data/wifi.wpa_key_mgmt.tmp")
    file.remove("data/wifi.wpa_pairwise.tmp")
    file.remove("data/wifi.rsn_pairwise.tmp")
    
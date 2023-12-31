import modules.executor as executor
import modules.fio as file
import modules.ui as ui

def run():
    wanInterface: str = file.read("data/wan.interface")
    wifiInterface: str = file.read("data/wifi.interface")
    
    next: bool = ui.yesno(f"Enabling Post Routing to WAN interface {wanInterface} and WiFi interface {wifiInterface}. Continue?", "Enable NAT")
    if not next: return
    executor.exec(executor.args(f"sudo iptables -t nat -A POSTROUTING -o {wanInterface} -j MASQUERADE"))
    
    next: bool = ui.yesno(f"Enabling Forwarding from WAN interface {wanInterface} to WiFi interface {wifiInterface}. Continue?", "Enable NAT")
    if not next: return
    executor.exec(executor.args(f"sudo iptables -A FORWARD -i {wanInterface} -o {wifiInterface} -m state --state RELATED,ESTABLISHED -j ACCEPT"))
    
    next: bool = ui.yesno(f"Enabling Forwarding from WiFi interface {wifiInterface} to WAN interface {wanInterface}. Continue?", "Enable NAT")
    if not next: return
    executor.exec(executor.args(f"sudo iptables -A FORWARD -i {wifiInterface} -o {wanInterface} -j ACCEPT"))
    
    ui.msgBox("NAT Enabled!", "Success")
    
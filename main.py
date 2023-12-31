import sys

from modules.executor import exec, args

import tasks.compatibility as compatibility
import tasks.packages as packages

compatibility.check(hasForce="--force" in sys.argv)
packages.check()

import modules.ui as ui

import tasks.selectwan as selectwan
import tasks.selectwifi as selectwifi
import tasks.configwifi as configwifi
import tasks.configdhcp as configdhcp
import tasks.assignip as assignip
import tasks.apply as apply
import tasks.servicectl as servicectl
import tasks.enablenat as enablenat
import tasks.otherutils as otherutils

while(True):
    
    selected: int = ui.menu([
        "Select WAN (internet) interface",
        "Select WiFi interface",
        "Configure WiFi",
        "DHCP Settings",
        "Assign IP Address",
        "Apply settings to configuration files",
        "Service Controls",
        "Enable NAT",
        "Other Utilities",
        "Exit"
    ], "Routered Ubuntu Control Panel", height=30)

    if selected == 0:
        selectwan.run()
        
    elif selected == 1:
        selectwifi.run()
        
    elif selected == 2:
        configwifi.run()
        
    elif selected == 3:
        configdhcp.run()
        
    elif selected == 4:
        assignip.run()

    elif selected == 5:
        apply.run()
        
    elif selected == 6:
        servicectl.run()
        
    elif selected == 7:
        enablenat.run()
        
    elif selected == 8:
        otherutils.run()
        
    elif selected == 9:
        exec(args("clear"))
        exit(0)
        
        
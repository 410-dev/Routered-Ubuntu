import os

def networkInterfaces(allDevices: bool) -> list:
    if allDevices:
        return os.listdir("/sys/class/net")
    else:
        return [interface for interface in os.listdir("/sys/class/net") if interface != "lo"]
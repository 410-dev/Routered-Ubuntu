import modules.fio as file
import modules.ui as ui
import modules.executor as executor

def run():
    options_main: dict = {
        "Start": "start",
        "Stop" : "stop",
        "Restart" : "restart",
        "Enable" : "enable",
        "Disable" : "disable",
        "Exit" : "exit"
    }
    
    options_main_list: list = list(options_main.keys())
    
    options_service: dict = {
        "All": "all",
        "DHCP Server": "isc-dhcp-server",
        "Hostapd" : "hostapd",
        "Exit": "exit"
    }
    
    options_service_list: list = list(options_service.keys())
    
    selection_action: int = ui.menu(options_main_list, "Service Controls - Action", height=20)    
    if selection_action == len(options_main_list) - 1:
        return
    
    selection_service: int = ui.menu(options_service_list, "Service Controls - Service", height=20)
    if selection_service == len(options_service_list) - 1:
        return
    
    cmdstruct: str = "sudo systemctl $action $service"

    action: str = options_main[options_main_list[selection_action]]
    service: str = options_service[options_service_list[selection_service]]
    
    failed: list = []
    
    if service == "all":
        for service in options_service.values():
            if service == "exit" or service == "all":
                continue
            output = executor.exec(executor.args(cmdstruct.replace("$action", action).replace("$service", service)))
            if output[0] != 0:
                failed.append(service)
    else:
        output = executor.exec(executor.args(cmdstruct.replace("$action", action).replace("$service", service)))
        if output[0] != 0:
            failed.append(service)
            
    if len(failed) > 0:
        failedTraces: list = []
        for service in failed:
            out2 = executor.exec(executor.args(f"sudo systemctl status {service}"))[1]
            failedTraces.append((service, out2))
        ui.msgBox(f"Failed to {action} services: {', '.join(failed)}\n\nPlease check your configuration or compatibility.\n\nThe next message box will show the journal.", "Error")
        for trace in failedTraces:
            ui.msgBox(f"{trace[1]}", title=f"Journal - {trace[0]}", height=35, width=70)
    else:
        ui.msgBox(f"Service {action}ed!", "Success")
    
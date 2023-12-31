import modules.ui as ui

def run():
    defaultOptions = {
        "Load settings from configuration files": "load",
        "Manually edit settings": "edit",
        "The Onion Router": "onion",
        "OpenVPN Server": "openvpnsrv",
        "Exit": "exit"
    }
    
    selection: int = ui.menu(defaultOptions.keys(), height=20, title="Select utility")
    
    if selection == len(defaultOptions.keys()) - 1:
        return
    
    selected: str = defaultOptions[list(defaultOptions.keys())[selection]]
    
    import importlib
    packagePath = f"tasks.{selected}"
    module = importlib.import_module(packagePath)
    module.run()
    
    return

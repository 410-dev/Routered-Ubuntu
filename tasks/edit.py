import modules.ui as ui
import modules.fio as file
from modules.executor import exec, args

def run():
    files: list = file.list("map")
    files.append("Exit")
    
    selection: int = ui.menu(files, height=20, title="Select configuration to edit")
    if selection == len(files) - 1:
        return
    
    mapfile: str = files[selection]
    mapfile = file.read(f"map/{mapfile}")
    
    exec(args(f"sudo nano {mapfile}"))
    
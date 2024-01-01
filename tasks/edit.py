import modules.ui as ui
import modules.fio as file
from modules.executor import exec, args, execInteractive

def run():
    files: list = file.list("map")
    files.append("Exit")
    
    selection: int = ui.menu(files, height=20, title="Select configuration to edit")
    if selection == len(files) - 1:
        return
    
    mapfile: str = files[selection]
    mapfile = file.read(f"map/{mapfile}")

    editor: dict = {
        "Nano": "nano $file",
        "Vim": "vim $file",
        "Vi": "vi $file",
        "Emacs": "emacs $file",
        "Exit": "exit"
    }

    selection: int = ui.menu(list(editor.keys()), height=20, title="Select editor")

    if selection == len(editor) - 1:
        return
    
    # Check if the editor is available
    editorExec = list(editor.values())[selection].split(" ")[0]
    if exec(args(f"which {editorExec}"))[0] != 0:
        doInstall: bool = ui.yesno("The selected editor is not installed. Would you like to install it?")
        if doInstall:
            result = exec(args(f"sudo apt install -y {list(editor.values())[selection].split(' ')[0]}"))
            if result[0] != 0:
                ui.msgBox(f"Failed to install {list(editor.values())[selection].split(' ')[0]}. Error: {result[2]}")
            else:
                ui.msgBox(f"Successfully installed {list(editor.values())[selection].split(' ')[0]}")
                return
        else:
            return
    
    # Replace $file with the mapfile
    commandline = list(editor.values())[selection].replace("$file", mapfile)
    execInteractive(args(commandline))

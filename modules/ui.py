import subprocess

def menu(options, title: str = "Select an option:", width: int = 50, height: int = 10):
    # Command parts
    
    # Get longest option
    longest = 0
    for option in options:
        if len(option) > longest:
            longest = len(option)
            
    # Calculate width
    width = longest + 10 if longest + 10 > width else width
    
    cmd = ['dialog', '--clear', '--stdout', '--menu', title, str(height), str(width), str(len(options))]

    # Add options to the command
    for index, option in enumerate(options):
        cmd.extend([str(index), option])  # Using index directly

    # Execute the dialog command
    try:
        output = subprocess.check_output(cmd, text=True)
        selected_index = int(output.strip())  # Parse the selected index
        return selected_index
    except subprocess.CalledProcessError as e:
        return -1  # None if user cancels or closes the dialog

def msgBox(text: str, title: str = "Message", width: int = 50, height: int = 10):
    cmd = ['dialog', '--clear', '--msgbox', text, str(height), str(width)]
    process = subprocess.run(cmd)
    return process.returncode == 0

def yesno(text: str, title: str = "Question", width: int = 50, height: int = 10) -> bool:
    cmd = ['dialog', '--clear', '--yesno', text, str(height), str(width)]
    process = subprocess.run(cmd)
    return process.returncode == 0


def read(prompt: str, default: str = "", width: int = 50, height: int = 10) -> str:
    cmd = ['dialog', '--clear', '--stdout', '--inputbox', prompt, str(height), str(width), default]
    try:
        result = subprocess.check_output(cmd, text=True)
        return result.strip() if result else default
    except subprocess.CalledProcessError:
        return default  # Return default if cancelled


def readSecure(prompt: str, default: str = "", width: int = 50, height: int = 10) -> str:
    cmd = ['dialog', '--clear', '--stdout', '--passwordbox', prompt, str(height), str(width)]
    try:
        result = subprocess.check_output(cmd, text=True)
        return result.strip() if result else default
    except subprocess.CalledProcessError:
        return default  # Return default if cancelled

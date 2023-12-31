import os
def read(file_path: str) -> str:
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content


def write(file_path: str, content: str) -> None:
    with open(file_path, 'w') as file:
        file.write(content)


def exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def remove(file_path: str) -> None:
    try:
        os.remove(file_path)
    except:
        pass
import subprocess

def exec(args: list) -> (int, str, str):
    try:
        result = subprocess.run(args, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, '', str(e)

def args(string: str) -> list:
    result = []
    current = ''
    in_quotes = False
    
    if string == None or string == '':
        return result

    for char in string:
        if char == '"' or char == "'":
            if in_quotes:
                result.append(current)
                current = ''
            in_quotes = not in_quotes
        else:
            if not in_quotes and char == ' ':
                result.append(current)
                current = ''
            else:
                current += char
                

    if current:
        result.append(current)

    return result


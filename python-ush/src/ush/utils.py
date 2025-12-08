def is_empty_string(s):
    return s.strip() == ""

def split_command(command):
    import shlex
    return shlex.split(command)

def log_message(message):
    import sys
    sys.stderr.write(f"[LOG] {message}\n")

def format_command_output(output):
    return output.strip() if output else "No output"

def parse_environment_variable(var):
    if '=' in var:
        key, value = var.split('=', 1)
        return key.strip(), value.strip()
    return var.strip(), None

def is_valid_command(command):
    return not is_empty_string(command) and not command.startswith('#')

def get_command_name(command):
    return command.split()[0] if command else None

def print_error(message):
    import sys
    sys.stderr.write(f"[ERROR] {message}\n")
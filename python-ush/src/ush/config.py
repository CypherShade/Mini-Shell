# config.py

import os

def load_rc_file():
    rc_file_path = os.path.expanduser("~/.ushrc")
    if os.path.exists(rc_file_path):
        with open(rc_file_path, 'r') as rc_file:
            return rc_file.readlines()
    return []

def parse_rc_lines(lines):
    config = {}
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):  # Ignore empty lines and comments
            key, _, value = line.partition('=')
            config[key.strip()] = value.strip()
    return config

def load_user_config():
    rc_lines = load_rc_file()
    return parse_rc_lines(rc_lines)
import shlex

def tokenize_command(command):
    return shlex.split(command)

def parse_command(command):
    # Check for pipeline first
    if '|' in command:
        return parse_pipeline(command)
    
    # Check for background execution
    background = command.strip().endswith('&')
    if background:
        command = command.strip()[:-1].strip()
    
    tokens = tokenize_command(command)
    if not tokens:
        return []
    
    command_structure = {
        'command': tokens[0],
        'args': [],
        'redirects': [],
        'background': background
    }
    
    # Handle I/O redirection
    i = 1
    while i < len(tokens):
        if tokens[i] in ('>', '>>', '<', '2>', '2>>'):
            if i + 1 < len(tokens):
                command_structure['redirects'].append((tokens[i], tokens[i + 1]))
                i += 2
            else:
                i += 1
        elif tokens[i] == '2>&1':
            # Special case for stderr to stdout
            command_structure['redirects'].append(('2>&1', ''))
            i += 1
        else:
            command_structure['args'].append(tokens[i])
            i += 1
    
    return [command_structure]

def parse_pipeline(command):
    # Check for background execution first
    background = command.strip().endswith('&')
    if background:
        command = command.strip()[:-1].strip()
    
    # Split by pipe
    pipe_parts = command.split('|')
    commands = []
    
    for i, part in enumerate(pipe_parts):
        part = part.strip()
        tokens = tokenize_command(part)
        
        if not tokens:
            continue
        
        command_structure = {
            'command': tokens[0],
            'args': [],
            'redirects': [],
            'background': background if i == len(pipe_parts) - 1 else False,
            'is_pipeline': True,
            'pipeline_position': i
        }
        
        # Handle I/O redirection
        j = 1
        while j < len(tokens):
            if tokens[j] in ('>', '>>', '<', '2>', '2>>'):
                if j + 1 < len(tokens):
                    command_structure['redirects'].append((tokens[j], tokens[j + 1]))
                    j += 2
                else:
                    j += 1
            elif tokens[j] == '2>&1':
                command_structure['redirects'].append(('2>&1', ''))
                j += 1
            else:
                command_structure['args'].append(tokens[j])
                j += 1
        
        commands.append(command_structure)
    
    return commands
import subprocess
import os
import sys
import shlex
import tempfile
import re
from .builtin import builtin_commands

# Global job_manager reference
_job_manager = None

def set_job_manager(job_manager):
    """Set the global job manager for the executor."""
    global _job_manager
    _job_manager = job_manager

def expand_command_substitution(command_str):
    """Expand $(command) and `command` substitutions."""
    # Pattern for $(command) and `command`
    pattern_dollar = r'\$\(([^)]+)\)'
    pattern_backtick = r'`([^`]+)`'
    
    def replace_substitution(match):
        cmd = match.group(1)
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Command substitution error: {e}", file=sys.stderr)
            return ""
    
    # Expand $(command)
    command_str = re.sub(pattern_dollar, replace_substitution, command_str)
    # Expand `command`
    command_str = re.sub(pattern_backtick, replace_substitution, command_str)
    
    return command_str

def execute_command(command_structure):
    # Handle I/O redirection setup (for both built-in and external commands)
    stdin = None
    stdout = None
    stderr = None
    files_to_close = []
    
    # Save original stdin/stdout/stderr for builtin commands
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    for redirect_type, filename in command_structure['redirects']:
        # Expand command substitutions in filenames
        filename = expand_command_substitution(filename)
        
        if redirect_type == '>':
            stdout = open(filename, 'w')
            files_to_close.append(stdout)
        elif redirect_type == '>>':
            stdout = open(filename, 'a')
            files_to_close.append(stdout)
        elif redirect_type == '<':
            stdin = open(filename, 'r')
            files_to_close.append(stdin)
        elif redirect_type == '2>':
            stderr = open(filename, 'w')
            files_to_close.append(stderr)
        elif redirect_type == '2>>':
            stderr = open(filename, 'a')
            files_to_close.append(stderr)
        elif redirect_type == '2>&1':
            # Redirect stderr to stdout
            stderr = subprocess.STDOUT
    
    try:
        # Handle builtin commands
        if command_structure['command'] in builtin_commands:
            # Redirect sys.stdout/stderr for builtin commands
            if stdout:
                sys.stdout = stdout
            if stderr and stderr != subprocess.STDOUT:
                sys.stderr = stderr
            if stdin:
                sys.stdin = stdin
            
            try:
                builtin_commands[command_structure['command']](command_structure['args'])
                return 0
            finally:
                # Restore original streams
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                sys.stdin = original_stdin
        
        # Expand command substitutions in arguments for external commands
        expanded_args = []
        for arg in command_structure['args']:
            expanded_args.append(expand_command_substitution(arg))
        
        # Prepare command arguments
        args = [command_structure['command']] + expanded_args
        command_str = ' '.join(args)
    
        # Execute the external command
        try:
            if command_structure['background']:
                process = subprocess.Popen(args, stdin=stdin, stdout=stdout, stderr=stderr)
                job_id = _job_manager.add_job(command_str, process) if _job_manager else None
                if job_id:
                    print(f"[{job_id}] {process.pid}")
                else:
                    print(f"[Background] PID: {process.pid}")
                return process.pid
            else:
                result = subprocess.run(args, stdin=stdin, stdout=stdout, stderr=stderr)
                return result.returncode
        except FileNotFoundError:
            print(f"ush: command not found: {command_structure['command']}")
            return 127
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            return 1
    finally:
        # Close all opened file handles
        for f in files_to_close:
            if f and hasattr(f, 'close'):
                try:
                    f.flush()
                    f.close()
                except:
                    pass

def execute_pipeline(commands):
    """Execute a pipeline of commands."""
    if not commands:
        return 1
    
    # Single command - no pipeline
    if len(commands) == 1:
        return execute_command(commands[0])
    
    processes = []
    previous_stdout = None
    
    try:
        for i, cmd in enumerate(commands):
            is_last = (i == len(commands) - 1)
            is_first = (i == 0)
            
            # Prepare command arguments
            args = [cmd['command']] + cmd['args']
            
            # Set up stdin
            stdin = previous_stdout if not is_first else None
            
            # Set up stdout
            if is_last:
                # Last command: use normal output or redirects
                stdout = None
                for redirect_type, filename in cmd['redirects']:
                    if redirect_type == '>':
                        stdout = open(filename, 'w')
                    elif redirect_type == '>>':
                        stdout = open(filename, 'a')
            else:
                # Intermediate command: pipe to next command
                stdout = subprocess.PIPE
            
            # Create process
            process = subprocess.Popen(
                args,
                stdin=stdin,
                stdout=stdout,
                stderr=subprocess.PIPE if not is_last else None
            )
            
            processes.append(process)
            
            # Close previous stdout
            if previous_stdout:
                previous_stdout.close()
            
            # Set up for next iteration
            previous_stdout = process.stdout
        
        # Wait for all processes to complete
        exit_code = 0
        for process in processes:
            process.wait()
            if process.returncode != 0:
                exit_code = process.returncode
        
        return exit_code
        
    except FileNotFoundError as e:
        print(f"ush: command not found in pipeline", file=sys.stderr)
        return 127
    except Exception as e:
        print(f"Error executing pipeline: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up any open file handles
        if previous_stdout:
            previous_stdout.close()

def handle_background_jobs():
    import os
    import signal

    def sigchld_handler(signum, frame):
        while True:
            try:
                pid, _ = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break
            except ChildProcessError:
                break

    # Only set up signal handler on Unix-like systems
    if hasattr(signal, 'SIGCHLD'):
        signal.signal(signal.SIGCHLD, sigchld_handler)
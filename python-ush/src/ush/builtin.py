import os
import sys
import shutil
import signal as sig_module
try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

# Global job_manager reference (will be set by shell)
_job_manager = None

# Global aliases dictionary
_aliases = {}

def set_job_manager(job_manager):
    """Set the global job manager for builtin commands."""
    global _job_manager
    _job_manager = job_manager

def cd(args):
    """Change the current directory."""
    try:
        if not args:
            target_dir = os.path.expanduser("~")
        else:
            target_dir = os.path.expanduser(args[0])
        os.chdir(target_dir)
    except Exception as e:
        print(f"cd: {e}")

def exit_shell(args):
    """Exit the shell."""
    sys.exit(0)

def export(args):
    """Set environment variables."""
    import os
    if len(args) == 1:
        key_value = args[0].split('=', 1)
        if len(key_value) == 2:
            os.environ[key_value[0]] = key_value[1]
        else:
            print("export: Invalid format. Use KEY=VALUE.")
    else:
        print("export: Usage: export KEY=VALUE")

def unset(args):
    """Unset environment variables."""
    for var in args:
        os.environ.pop(var, None)

def help_command(args):
    """Display help information about built-in commands."""
    help_text = {
        'cd': 'cd [directory] - Change the current directory',
        'exit': 'exit - Exit the shell',
        'export': 'export VAR=value - Set environment variable',
        'unset': 'unset VAR - Unset environment variable',
        'history': 'history [n] - Show command history (last n commands)',
        'jobs': 'jobs - List background jobs',
        'fg': 'fg <job_id> - Bring job to foreground',
        'bg': 'bg <job_id> - Send job to background',
        'help': 'help [command] - Show help information',
    }
    
    if not args:
        print("Built-in commands:")
        print()
        for cmd, desc in sorted(help_text.items()):
            print(f"  {desc}")
        print()
        print("Shell features:")
        print("  I/O Redirection: > >> <")
        print("  Pipelines: command1 | command2")
        print("  Background jobs: command &")
        print("  Command substitution: $(command)")
        print()
        print("Type 'help <command>' for more information on a specific command.")
    else:
        cmd = args[0]
        if cmd in help_text:
            print(help_text[cmd])
        else:
            print(f"help: no help topics match '{cmd}'")

def history(args):
    """Show command history."""
    if not readline:
        print("history: readline not available")
        return
    
    hist_len = readline.get_current_history_length()
    
    # Determine how many lines to show
    if args and args[0].isdigit():
        num_lines = int(args[0])
        start = max(1, hist_len - num_lines + 1)
    else:
        start = 1
    
    # Display history
    for i in range(start, hist_len + 1):
        line = readline.get_history_item(i)
        if line:
            print(f"{i:5d}  {line}")

def jobs(args):
    """List background jobs."""
    if _job_manager is None:
        print("jobs: Job manager not initialized")
        return
    
    _job_manager.update_jobs()
    active_jobs = _job_manager.get_jobs()
    
    if not active_jobs:
        print("No active jobs")
        return
    
    for job_id, job in active_jobs.items():
        status = "Running" if job.status == "running" else "Stopped"
        print(f"[{job_id}]  {status}\t\t{job.command}")

def fg(args):
    """Bring a background job to the foreground."""
    if _job_manager is None:
        print("fg: Job manager not initialized")
        return
    
    if not args:
        print("fg: usage: fg <job_id>")
        return
    
    try:
        job_id = int(args[0])
    except ValueError:
        print(f"fg: {args[0]}: no such job")
        return
    
    if job_id not in _job_manager.jobs:
        print(f"fg: {job_id}: no such job")
        return
    
    job = _job_manager.jobs[job_id]
    print(f"[{job_id}]  {job.command}")
    
    # Wait for the job to complete
    try:
        job.process.wait()
        _job_manager.remove_job(job_id)
    except KeyboardInterrupt:
        print("\nJob interrupted")

def bg(args):
    """Send a job to the background."""
    if _job_manager is None:
        print("bg: Job manager not initialized")
        return
    
    if not args:
        print("bg: usage: bg <job_id>")
        return
    
    try:
        job_id = int(args[0])
    except ValueError:
        print(f"bg: {args[0]}: no such job")
        return
    
    if job_id not in _job_manager.jobs:
        print(f"bg: {job_id}: no such job")
        return
    
    job = _job_manager.jobs[job_id]
    print(f"[{job_id}]  {job.command} &")
    # In a real shell, we'd send SIGCONT here
    # For now, just mark it as running
    job.status = 'running'

# ============================================
# PURE PYTHON COMMANDS
# ============================================

def cmd_cat(args):
    """Display file contents."""
    if not args:
        try:
            for line in sys.stdin:
                print(line, end='')
        except KeyboardInterrupt:
            pass
        return 0
    
    for filename in args:
        try:
            with open(filename, 'r') as f:
                print(f.read(), end='')
        except FileNotFoundError:
            print(f"cat: {filename}: No such file or directory", file=sys.stderr)
            return 1
        except PermissionError:
            print(f"cat: {filename}: Permission denied", file=sys.stderr)
            return 1
    return 0

def cmd_ls(args):
    """List directory contents."""
    path = args[0] if args else '.'
    
    try:
        items = sorted(os.listdir(path))
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                print(f"{item}/")
            else:
                print(item)
        return 0
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"ls: cannot open directory '{path}': Permission denied", file=sys.stderr)
        return 1

def cmd_echo(args):
    """Print arguments."""
    print(' '.join(args))
    return 0

def cmd_pwd(args):
    """Print working directory."""
    print(os.getcwd())
    return 0

def cmd_mkdir(args):
    """Create directories."""
    if not args:
        print("mkdir: missing operand", file=sys.stderr)
        return 1
    
    for dirname in args:
        try:
            os.makedirs(dirname, exist_ok=True)
        except Exception as e:
            print(f"mkdir: cannot create directory '{dirname}': {e}", file=sys.stderr)
            return 1
    return 0

def cmd_rm(args):
    """Remove files or directories."""
    if not args:
        print("rm: missing operand", file=sys.stderr)
        return 1
    
    recursive = '-r' in args or '-rf' in args
    force = '-f' in args or '-rf' in args
    
    files = [arg for arg in args if not arg.startswith('-')]
    
    for filename in files:
        try:
            if os.path.isdir(filename):
                if recursive:
                    shutil.rmtree(filename)
                else:
                    print(f"rm: cannot remove '{filename}': Is a directory", file=sys.stderr)
                    if not force:
                        return 1
            else:
                os.remove(filename)
        except FileNotFoundError:
            if not force:
                print(f"rm: cannot remove '{filename}': No such file or directory", file=sys.stderr)
                return 1
        except Exception as e:
            print(f"rm: cannot remove '{filename}': {e}", file=sys.stderr)
            if not force:
                return 1
    return 0

def cmd_cp(args):
    """Copy files."""
    if len(args) < 2:
        print("cp: missing file operand", file=sys.stderr)
        return 1
    
    src, dest = args[0], args[1]
    try:
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(src))
        shutil.copy2(src, dest)
        return 0
    except Exception as e:
        print(f"cp: cannot copy '{src}' to '{dest}': {e}", file=sys.stderr)
        return 1

def cmd_mv(args):
    """Move/rename files."""
    if len(args) < 2:
        print("mv: missing file operand", file=sys.stderr)
        return 1
    
    src, dest = args[0], args[1]
    try:
        shutil.move(src, dest)
        return 0
    except Exception as e:
        print(f"mv: cannot move '{src}' to '{dest}': {e}", file=sys.stderr)
        return 1

def cmd_touch(args):
    """Create empty file or update timestamp."""
    if not args:
        print("touch: missing file operand", file=sys.stderr)
        return 1
    
    for filename in args:
        try:
            with open(filename, 'a'):
                os.utime(filename, None)
        except Exception as e:
            print(f"touch: cannot touch '{filename}': {e}", file=sys.stderr)
            return 1
    return 0

def cmd_grep(args):
    """Search for pattern in files."""
    if not args:
        print("grep: missing pattern", file=sys.stderr)
        return 1
    
    pattern = args[0]
    files = args[1:] if len(args) > 1 else ['-']
    
    found = False
    for filename in files:
        try:
            if filename == '-':
                lines = sys.stdin.readlines()
            else:
                with open(filename, 'r') as f:
                    lines = f.readlines()
            
            for line in lines:
                if pattern in line:
                    if len(files) > 1 and filename != '-':
                        print(f"{filename}:{line}", end='')
                    else:
                        print(line, end='')
                    found = True
        except FileNotFoundError:
            print(f"grep: {filename}: No such file or directory", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"grep: {filename}: {e}", file=sys.stderr)
            return 1
    return 0 if found else 1

def cmd_wc(args):
    """Count lines, words, characters."""
    if not args:
        text = sys.stdin.read()
        lines = text.count('\n')
        words = len(text.split())
        chars = len(text)
        print(f"{lines} {words} {chars}")
        return 0
    
    total_lines = total_words = total_chars = 0
    
    for filename in args:
        try:
            with open(filename, 'r') as f:
                text = f.read()
                lines = text.count('\n')
                words = len(text.split())
                chars = len(text)
                print(f"{lines:8} {words:8} {chars:8} {filename}")
                total_lines += lines
                total_words += words
                total_chars += chars
        except Exception as e:
            print(f"wc: {filename}: {e}", file=sys.stderr)
            return 1
    
    if len(args) > 1:
        print(f"{total_lines:8} {total_words:8} {total_chars:8} total")
    return 0

# ============================================
# ADDITIONAL BUILT-IN COMMANDS
# ============================================

def alias_command(args):
    """Create command aliases."""
    global _aliases
    
    if not args:
        if not _aliases:
            print("No aliases defined")
        else:
            for name, value in sorted(_aliases.items()):
                print(f"alias {name}='{value}'")
        return 0
    
    alias_def = ' '.join(args)
    if '=' in alias_def:
        name, value = alias_def.split('=', 1)
        name = name.strip()
        value = value.strip().strip("'\"")
        _aliases[name] = value
        print(f"Alias created: {name} -> {value}")
    else:
        if args[0] in _aliases:
            print(f"alias {args[0]}='{_aliases[args[0]]}'")
        else:
            print(f"alias: {args[0]}: not found", file=sys.stderr)
            return 1
    return 0

def env_command(args):
    """List all environment variables."""
    for key, value in sorted(os.environ.items()):
        print(f"{key}={value}")
    return 0

def kill_command(args):
    """Terminate a job or process."""
    if not args:
        print("kill: missing job or process ID", file=sys.stderr)
        return 1
    
    if not _job_manager:
        print("kill: job manager not initialized", file=sys.stderr)
        return 1
    
    try:
        job_id = int(args[0])
        
        if job_id in _job_manager.jobs:
            job = _job_manager.jobs[job_id]
            try:
                job.process.terminate()
                print(f"[{job_id}] Terminated: {job.command}")
                _job_manager.remove_job(job_id)
                return 0
            except Exception as e:
                print(f"kill: failed to terminate job {job_id}: {e}", file=sys.stderr)
                return 1
        else:
            try:
                os.kill(job_id, sig_module.SIGTERM)
                print(f"Process {job_id} terminated")
                return 0
            except ProcessLookupError:
                print(f"kill: ({job_id}) - No such process", file=sys.stderr)
                return 1
            except PermissionError:
                print(f"kill: ({job_id}) - Operation not permitted", file=sys.stderr)
                return 1
    except ValueError:
        print(f"kill: {args[0]}: arguments must be process or job IDs", file=sys.stderr)
        return 1

builtin_commands = {
    # Core built-ins
    'cd': cd,
    'exit': exit_shell,
    'export': export,
    'unset': unset,
    'history': history,
    'jobs': jobs,
    'fg': fg,
    'bg': bg,
    'help': help_command,
    'alias': alias_command,
    'env': env_command,
    'kill': kill_command,
    # Pure Python commands
    'cat': cmd_cat,
    'ls': cmd_ls,
    'echo': cmd_echo,
    'pwd': cmd_pwd,
    'mkdir': cmd_mkdir,
    'rm': cmd_rm,
    'cp': cmd_cp,
    'mv': cmd_mv,
    'touch': cmd_touch,
    'grep': cmd_grep,
    'wc': cmd_wc,
}
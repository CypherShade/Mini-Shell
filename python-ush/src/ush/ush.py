import os
import sys
import signal
try:
    import readline
except ImportError:
    # Windows doesn't have readline, use pyreadline3 or basic input
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None
from .config import load_rc_file
from .parser import parse_command
from .executor import execute_command, execute_pipeline, set_job_manager as set_executor_job_manager
from .jobs import JobManager
from .builtin import set_job_manager as set_builtin_job_manager

class Shell:
    def __init__(self, pure_mode=False, interactive=True):
        self.pure_mode = pure_mode
        self.interactive = interactive
        self.job_manager = JobManager()
        # Set job manager for executor and builtins
        set_executor_job_manager(self.job_manager)
        set_builtin_job_manager(self.job_manager)
        self.history_file = os.path.expanduser("~/.ush_history")
        
        if self.interactive:
            self.load_history()
            load_rc_file()
            signal.signal(signal.SIGINT, self.signal_handler)
            
            # Print mode information
            if self.pure_mode:
                print("🐍 USH Shell - Pure Python Mode")
                print("Only built-in Python commands available.\n")
            else:
                print("💻 USH Shell - Hybrid Mode")
                print("Python built-ins + system commands available.\n")

    def load_history(self):
        if readline and os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)

    def save_history(self):
        if readline:
            readline.write_history_file(self.history_file)

    def signal_handler(self, signum, frame):
        print("\nExiting shell...")
        self.save_history()
        exit(0)
    
    def execute_script(self, script_path):
        """Execute commands from a script file."""
        try:
            with open(script_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    if self.interactive:
                        print(f"ush:{line_num}> {line}")
                    
                    try:
                        commands = parse_command(line)
                        
                        # Check if this is a pipeline
                        if len(commands) > 1 and any(cmd.get('is_pipeline') for cmd in commands):
                            execute_pipeline(commands)
                        else:
                            for command in commands:
                                execute_command(command)
                    except Exception as e:
                        print(f"Error at line {line_num}: {e}", file=sys.stderr)
                        if not self.interactive:
                            return 1
            return 0
        except FileNotFoundError:
            print(f"ush: {script_path}: No such file or directory", file=sys.stderr)
            return 127
        except PermissionError:
            print(f"ush: {script_path}: Permission denied", file=sys.stderr)
            return 126

    def run(self):
        while True:
            try:
                # Update job statuses and clean up completed jobs
                self.job_manager.update_jobs()
                completed_jobs = [job_id for job_id, job in self.job_manager.jobs.items() if job.is_completed()]
                for job_id in completed_jobs:
                    job = self.job_manager.jobs[job_id]
                    print(f"[{job_id}]  Done\t\t{job.command}")
                    self.job_manager.remove_job(job_id)
                
                cwd = os.getcwd()
                home = os.path.expanduser("~")
                if cwd.startswith(home):
                    display_path = "~" + cwd[len(home):]
                else:
                    display_path = cwd
                command_line = input(f"ush:{display_path}> ")
                if command_line.strip() == "":
                    continue
                if readline:
                    readline.add_history(command_line)
                commands = parse_command(command_line)
                
                # Check if this is a pipeline
                if len(commands) > 1 and any(cmd.get('is_pipeline') for cmd in commands):
                    execute_pipeline(commands)
                else:
                    for command in commands:
                        execute_command(command)
            except EOFError:
                print("\nExiting shell...")
                self.save_history()
                break
            except KeyboardInterrupt:
                print("\nUse 'exit' to leave the shell.")

def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='ush',
        description='USH - A Unix-like Shell implemented in Python',
        epilog='For more information, visit: https://github.com/CypherShade/Mini-Shell'
    )
    
    parser.add_argument(
        'script',
        nargs='?',
        help='Script file to execute (if not provided, starts interactive mode)'
    )
    
    parser.add_argument(
        '--pure',
        action='store_true',
        help='Run in pure Python mode (only built-in commands, no system commands)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='USH 1.0.0'
    )
    
    parser.add_argument(
        '-c',
        '--command',
        metavar='COMMAND',
        help='Execute command string and exit'
    )
    
    args = parser.parse_args()
    
    # Execute single command if -c is provided
    if args.command:
        shell = Shell(pure_mode=args.pure, interactive=False)
        commands = parse_command(args.command)
        
        if len(commands) > 1 and any(cmd.get('is_pipeline') for cmd in commands):
            execute_pipeline(commands)
        else:
            for command in commands:
                execute_command(command)
        return 0
    
    # Execute script if provided
    if args.script:
        shell = Shell(pure_mode=args.pure, interactive=False)
        return shell.execute_script(args.script)
    
    # Start interactive shell
    shell = Shell(pure_mode=args.pure, interactive=True)
    shell.run()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main() or 0)
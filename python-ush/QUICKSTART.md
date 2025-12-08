# Quick Start Guide - USH Shell

## 🚀 Installation (Choose One)

### Option 1: Docker (Recommended - 2 commands)
```bash
cd python-ush
docker-compose run --rm ush-shell
```

### Option 2: Manual (Ubuntu/Linux)
```bash
cd python-ush
pip3 install -r requirements.txt
PYTHONPATH=src python3 -m ush.ush
```

### Option 3: Manual (Windows)
```powershell
cd python-ush
pip install -r requirements.txt
$env:PYTHONPATH = "src"
python -m ush.ush
```

---

## 🎯 Common Commands

```bash
# Basic
help                    # Show all commands
pwd                     # Current directory
ls                      # List files
cd directory            # Change directory
cat file.txt            # Display file

# File Operations
touch file.txt          # Create file
cp file1 file2          # Copy file
mv old new              # Move/rename
rm file                 # Delete file
rm -rf directory        # Delete directory
mkdir dirname           # Create directory

# Text Processing
echo "text"             # Print text
grep "pattern" file     # Search in file
wc file.txt             # Count lines/words

# I/O Redirection
command > file          # Redirect output
command >> file         # Append output
command < file          # Input from file
command 2> errors.txt   # Redirect errors

# Pipelines
cat file | grep test    # Pipe commands
ls | wc -l              # Count files

# Background Jobs
sleep 100 &             # Run in background
jobs                    # List jobs
fg 1                    # Foreground job 1
bg 1                    # Background job 1
kill 1                  # Terminate job 1

# Environment
export VAR=value        # Set variable
env                     # List variables
unset VAR               # Remove variable

# Aliases
alias ll='ls -la'       # Create shortcut
alias                   # List aliases

# History
history                 # Show all commands
history 10              # Show last 10

# Exit
exit                    # Quit shell
```

---

## 🧪 Running Tests

```bash
# Using Docker
docker-compose run --rm ush-tests

# Manual
PYTHONPATH=src python3 -m pytest tests/ -v
```

---

## 🎬 Demo

```bash
# Run the demo script
python3 -m ush.ush demo.sh

# Or manually try:
ush:~> help
ush:~> ls
ush:~> echo "Hello" > test.txt
ush:~> cat test.txt
ush:~> cat test.txt | grep Hello
ush:~> rm test.txt
```

---

## 🐳 Docker Commands

```bash
# Run shell (hybrid mode)
docker-compose run --rm ush-shell

# Run shell (pure Python mode)
docker-compose run --rm ush-shell-pure

# Run tests
docker-compose run --rm ush-tests

# Run with coverage
docker-compose run --rm ush-coverage
```

---

## 💡 Advanced Features

```bash
# Execute script
python3 -m ush.ush script.sh

# Execute single command
python3 -m ush.ush -c "ls | grep test"

# Pure Python mode
python3 -m ush.ush --pure

# Command substitution
echo "Today is $(date)"
cat $(find . -name "*.txt")
```

---

## 🆘 Troubleshooting

**Problem:** Command not found  
**Solution:** In pure mode, only built-in commands work. Use hybrid mode or add command.

**Problem:** Tests fail  
**Solution:** Set PYTHONPATH: `export PYTHONPATH=src` (Linux) or `$env:PYTHONPATH = "src"` (Windows)

**Problem:** Can't run in Docker  
**Solution:** Make sure Docker is running: `docker --version`

---

## 📞 Quick Help

```bash
# Show version
python3 -m ush.ush --version

# Show help
python3 -m ush.ush --help

# In shell
ush:~> help
ush:~> help <command>
```

---

**For full documentation, see README.md**

# Complete Testing Guide for USH Shell

## ✅ All Issues Fixed!

### Fixed Issues:
1. ✅ File redirection tests now pass (builtin commands now respect I/O redirection)
2. ✅ Demo script runs successfully
3. ✅ All 20 tests passing

---

## 🚀 Quick Start - Run Everything

### Option 1: Using Docker (RECOMMENDED)

**Prerequisites:** Docker Desktop installed and running

```powershell
cd "c:\Users\Owais Haroon\Desktop\Mini-Shell\python-ush"

# Run all tests
docker-compose run --rm ush-tests

# Run the demo
docker-compose run --rm ush-demo

# Open interactive shell
docker-compose run --rm ush-shell

# Open interactive shell (pure Python mode - no system commands)
docker-compose run --rm ush-shell-pure
```

### Option 2: Using WSL Ubuntu

```bash
cd /mnt/c/Users/Owais\ Haroon/Desktop/Mini-Shell/python-ush

# Install dependencies
pip3 install -r requirements.txt

# Run tests
PYTHONPATH=src python3 -m pytest tests/ -v

# Run demo
PYTHONPATH=src python3 -m ush.ush demo.sh

# Open interactive shell
PYTHONPATH=src python3 -m ush.ush
```

### Option 3: Windows PowerShell (Native)

```powershell
cd "c:\Users\Owais Haroon\Desktop\Mini-Shell\python-ush"

# Install dependencies
pip install -r requirements.txt

# Run tests
$env:PYTHONPATH = "src"
python -m pytest tests/ -v

# Run demo
$env:PYTHONPATH = "src"
python -m ush.ush demo.sh

# Open interactive shell
$env:PYTHONPATH = "src"
python -m ush.ush
```

---

## 🧪 Testing Checklist

### 1. Automated Tests (20 tests)

```powershell
docker-compose run --rm ush-tests
```

**Expected Result:** All 20 tests should PASS
- ✅ 18 Parser and Job tests
- ✅ 2 Executor tests (file redirection - NOW FIXED!)

### 2. Demo Script

```powershell
docker-compose run --rm ush-demo
```

**Expected Output:**
- Basic commands (pwd)
- File operations (mkdir, touch, ls)
- I/O redirection (>, >>)
- Pipelines (|)
- Environment variables (export)
- Cleanup

### 3. Interactive Shell Testing

```powershell
docker-compose run --rm ush-shell
```

Once inside the shell, test each feature:

#### A. Basic Commands
```bash
help                    # Show all commands
pwd                     # Current directory
ls                      # List files
cd examples             # Change directory
cd ..                   # Go back
echo "Hello World"      # Print text
```

#### B. File Operations
```bash
mkdir test_dir
cd test_dir
touch file1.txt file2.txt
echo "Hello" > file1.txt
cat file1.txt
ls -la
cd ..
rm -rf test_dir
```

#### C. I/O Redirection (NOW WORKING!)
```bash
echo "Line 1" > test.txt
echo "Line 2" >> test.txt
cat test.txt
cat < test.txt
rm test.txt
```

#### D. Pipelines
```bash
ls | wc -l
echo "test\npattern\ntest" | grep "test"
cat ../README.md | grep "USH" | wc -l
```

#### E. Background Jobs
```bash
sleep 5 &               # Run in background
jobs                    # List jobs
# Wait a moment, then:
jobs                    # Job should be gone after completion
```

#### F. Environment Variables
```bash
export MY_VAR="Hello USH"
env | grep MY_VAR
echo $MY_VAR            # May not work - shell variable expansion
unset MY_VAR
```

#### G. Command History
```bash
history                 # View all history
history 5               # View last 5 commands
# Use UP/DOWN arrow keys to navigate
```

#### H. Aliases
```bash
alias ll='ls -la'
ll
alias
```

#### I. Command Substitution
```bash
echo "Current dir: $(pwd)"
echo "Files: $(ls | wc -l)"
```

#### J. Exit Shell
```bash
exit
# Or press Ctrl+D
```

---

## 📊 Test Results Summary

### All Tests Passing ✅

```
Platform: Linux (Docker Ubuntu 22.04)
Python: 3.10.12
Pytest: 9.0.2

tests/test_executor.py::TestExecutor::test_append_redirection PASSED
tests/test_executor.py::TestExecutor::test_background_job PASSED
tests/test_executor.py::TestExecutor::test_command_with_redirection PASSED
tests/test_executor.py::TestExecutor::test_invalid_command PASSED
tests/test_executor.py::TestExecutor::test_simple_command PASSED
tests/test_jobs.py::TestJobManager::test_add_job PASSED
tests/test_jobs.py::TestJobManager::test_get_jobs PASSED
tests/test_jobs.py::TestJobManager::test_job_completion PASSED
tests/test_jobs.py::TestJobManager::test_job_id_increment PASSED
tests/test_jobs.py::TestJobManager::test_remove_job PASSED
tests/test_jobs.py::TestJobManager::test_update_jobs PASSED
tests/test_parser.py::TestParser::test_background_command PASSED
tests/test_parser.py::TestParser::test_command_with_escape PASSED
tests/test_parser.py::TestParser::test_command_with_multiple_arguments PASSED
tests/test_parser.py::TestParser::test_command_with_pipe PASSED
tests/test_parser.py::TestParser::test_command_with_quotes PASSED
tests/test_parser.py::TestParser::test_command_with_redirection PASSED
tests/test_parser.py::TestParser::test_empty_command PASSED
tests/test_parser.py::TestParser::test_simple_command PASSED
tests/test_parser.py::TestParser::test_tokenize_command PASSED

20 passed in ~2s ✅
```

---

## 🐳 How Docker Works in This Project

### What Docker Does:
1. **Creates an isolated Linux environment** (Ubuntu 22.04)
2. **Installs Python 3.10** and all dependencies automatically
3. **Mounts your code** from Windows into the container
4. **Runs the shell** in a consistent Linux environment

### Docker vs WSL:
- **Docker:** Lightweight containers, isolated environments, easy to reset
- **WSL:** Full Linux subsystem, persistent, closer to native Linux

### Why Use Docker Here:
- ✅ No manual Python/dependency installation
- ✅ Consistent environment across all machines
- ✅ Easy cleanup (just delete containers)
- ✅ Works on Windows, Mac, and Linux identically

### Docker Compose Services:

| Service | Purpose | Command |
|---------|---------|---------|
| `ush-shell` | Interactive shell (hybrid mode) | `docker-compose run --rm ush-shell` |
| `ush-shell-pure` | Interactive shell (pure Python) | `docker-compose run --rm ush-shell-pure` |
| `ush-demo` | Run demo script | `docker-compose run --rm ush-demo` |
| `ush-tests` | Run all tests | `docker-compose run --rm ush-tests` |
| `ush-coverage` | Run tests with coverage | `docker-compose run --rm ush-coverage` |

---

## 🎯 Recommendation: Use Docker!

**Why Docker is best for this project:**
1. No need to configure WSL or native Python environment
2. Consistent Linux environment (the shell is designed for Linux)
3. Isolated from your system
4. Easy to reset if something breaks
5. Same commands work for everyone on the team

**Note:** Docker Desktop runs directly on Windows - WSL is NOT required!

---

## 📝 Quick Reference

### Most Common Commands

```powershell
# Run tests
docker-compose run --rm ush-tests

# Run demo
docker-compose run --rm ush-demo

# Open shell
docker-compose run --rm ush-shell

# Rebuild after code changes
docker-compose build
```

### Troubleshooting

**Problem:** "docker-compose: command not found"
**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop/

**Problem:** Tests fail or demo doesn't work
**Solution:** Rebuild the container:
```powershell
docker-compose build
docker-compose run --rm ush-tests
```

**Problem:** Container won't start
**Solution:** Make sure Docker Desktop is running

---

## ✨ Summary

Your Mini-Shell project is now **fully functional** with:
- ✅ All 20 automated tests passing
- ✅ File I/O redirection working correctly
- ✅ Demo script running successfully
- ✅ Interactive shell ready to use
- ✅ Docker setup complete and working

**You're ready to test and demo your project!** 🎉

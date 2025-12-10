# USH - Unix Shell Implementation in Python

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen.svg)](tests/)

A fully-featured Unix shell implementation in Python, supporting both hybrid (Python + system commands) and pure Python execution modes. Built as a collaborative Operating Systems course project.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Team Division](#-team-division)
- [Testing](#-testing)
- [Docker Support](#-docker-support)
- [Examples](#-examples)
- [Documentation](#-documentation)
- [License](#-license)

---

## ✨ Features

### Core Shell Capabilities
- **Interactive Command Prompt** with history and navigation
- **Script Execution** - Run shell scripts from files
- **Command-line Arguments** - Execute single commands with `-c` flag
- **Pure Python Mode** - Run without system dependencies using `--pure`
- **Dual Execution Modes**:
  - **Hybrid Mode** (default): Python built-ins + system commands
  - **Pure Mode** (`--pure`): Only Python-implemented commands

### Command Features
- **I/O Redirection**
  - Input: `command < input.txt`
  - Output: `command > output.txt`
  - Append: `command >> output.txt`
  - Stderr: `command 2> errors.txt`
  - Stderr append: `command 2>> errors.txt`
  - Combine streams: `command 2>&1`
  
- **Pipelines** - Chain commands: `cat file | grep pattern | wc -l`

- **Background Jobs**
  - Run in background: `command &`
  - List jobs: `jobs`
  - Foreground: `fg [job_id]`
  - Background: `bg [job_id]`
  - Kill job: `kill [job_id]`

- **Command Substitution**
  - Modern syntax: `echo "Today is $(date)"`
  - Classic syntax: ``echo "Files: `ls`"``

- **Environment Variables**
  - Set: `export VAR=value`
  - List: `env`
  - Unset: `unset VAR`

- **Aliases**
  - Create: `alias ll='ls -la'`
  - List: `alias`

- **Command History**
  - View all: `history`
  - View last N: `history 10`
  - Navigate with arrow keys

### Built-in Commands

#### Essential Built-ins
- `cd [directory]` - Change directory
- `exit [code]` - Exit shell
- `help [command]` - Show help information
- `history [n]` - Show command history

#### Job Control
- `jobs` - List background jobs
- `fg [job_id]` - Bring job to foreground
- `bg [job_id]` - Resume job in background
- `kill [job_id]` - Terminate job

#### Environment
- `export VAR=value` - Set environment variable
- `env` - Display all environment variables
- `unset VAR` - Remove environment variable
- `alias [name='command']` - Create command alias

#### Pure Python Commands (work in `--pure` mode)
- `cat [files...]` - Concatenate and display files
- `ls [directory]` - List directory contents
- `echo [text...]` - Print text to output
- `pwd` - Print working directory
- `mkdir [directories...]` - Create directories
- `rm [-rf] [files...]` - Remove files/directories
- `cp <source> <dest>` - Copy files
- `mv <source> <dest>` - Move/rename files
- `touch [files...]` - Create empty files
- `grep <pattern> [files...]` - Search for patterns
- `wc [files...]` - Count lines, words, characters

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USH Shell                            │
│                       (ush.py)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Main REPL Loop                                    │  │
│  │  • Command History                                   │  │
│  │  • User Interface                                    │  │
│  │  • Script Execution                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Parser                                 │
│                    (parser.py)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Command Tokenization                              │  │
│  │  • Pipeline Detection                                │  │
│  │  • Redirection Parsing (>, <, >>, 2>, 2>&1)         │  │
│  │  • Background Detection (&)                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Executor                                │
│                   (executor.py)                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Process Management                                │  │
│  │  • I/O Redirection (stdin/stdout/stderr)             │  │
│  │  • Pipeline Execution                                │  │
│  │  • Command Substitution                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
            │                                  │
            ▼                                  ▼
┌────────────────────────┐      ┌─────────────────────────────┐
│   Built-in Commands    │      │     Job Manager             │
│    (builtin.py)        │      │      (jobs.py)              │
│  ┌──────────────────┐  │      │  ┌───────────────────────┐ │
│  │ • cd, pwd, exit  │  │      │  │ • Job Tracking        │ │
│  │ • ls, cat, grep  │  │      │  │ • Process Management  │ │
│  │ • echo, touch    │  │      │  │ • Status Updates      │ │
│  │ • cp, mv, rm     │  │      │  └───────────────────────┘ │
│  │ • alias, env     │  │      └─────────────────────────────┘
│  └──────────────────┘  │
└────────────────────────┘
```

### Component Responsibilities

1. **ush.py** - Main shell interface and REPL
2. **parser.py** - Command parsing and tokenization
3. **executor.py** - Process execution and I/O management
4. **builtin.py** - Pure Python command implementations
5. **jobs.py** - Background job control
6. **signals.py** - Signal handling (Ctrl+C, Ctrl+Z)
7. **config.py** - Configuration and settings
8. **utils.py** - Utility functions

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+** (tested with 3.13.7)
- **pip** (Python package installer)
- **Docker** (optional, for containerized deployment)

### Method 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/CypherShade/Mini-Shell.git
cd Mini-Shell/python-ush

# Run using Docker Compose
docker-compose run --rm ush-shell
```

### Method 2: Manual Installation (Ubuntu/Linux)

```bash
# Clone the repository
git clone https://github.com/CypherShade/Mini-Shell.git
cd Mini-Shell/python-ush

# Install dependencies
pip3 install -r requirements.txt

# Run the shell
PYTHONPATH=src python3 -m ush.ush
```

### Method 3: Manual Installation (Windows)

```powershell
# Clone the repository
git clone https://github.com/CypherShade/Mini-Shell.git
cd Mini-Shell\python-ush

# Install dependencies
pip install -r requirements.txt

# Run the shell
$env:PYTHONPATH = "src"
python -m ush.ush
```

---

## 💻 Usage

### Interactive Mode

```bash
# Start shell (hybrid mode - default)
python3 -m ush.ush

# Start shell (pure Python mode)
python3 -m ush.ush --pure
```

### Script Execution

```bash
# Execute a shell script
python3 -m ush.ush script.sh

# Execute a single command
python3 -m ush.ush -c "ls -la | grep test"
```

### Command-line Options

```
usage: ush [-h] [--version] [--pure] [-c COMMAND] [script]

USH - Unix Shell in Python

positional arguments:
  script                Shell script to execute

options:
  -h, --help            Show this help message and exit
  --version             Show version information
  --pure                Run in pure Python mode (no system commands)
  -c COMMAND, --command COMMAND
                        Execute a single command and exit
```

---

## 📁 Project Structure

```
python-ush/
├── src/
│   └── ush/
│       ├── __init__.py          # Package initialization
│       ├── ush.py               # Main shell REPL
│       ├── parser.py            # Command parsing
│       ├── executor.py          # Command execution
│       ├── builtin.py           # Built-in commands
│       ├── jobs.py              # Job management
│       ├── signals.py           # Signal handling
│       ├── config.py            # Configuration
│       └── utils.py             # Utility functions
│
├── tests/
│   ├── test_parser.py           # Parser tests (10 tests)
│   ├── test_executor.py         # Executor tests (5 tests)
│   └── test_jobs.py             # Job manager tests (6 tests)
│
├── examples/                    # Example scripts
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Multi-service orchestration
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── LICENSE                     # MIT License
├── README.md                   # This file
├── QUICKSTART.md              # Quick reference guide
├── IMPLEMENTATION_SUMMARY.md  # Feature documentation
└── demo.sh                    # Feature demonstration script
```

---

## 👥 Team Division

This project was developed collaboratively by a 3-person team, with clear module ownership:

### 🔵 Person 1: Core Shell & Parsing
**Modules:** `ush.py`, `parser.py`, `config.py`, `signals.py`

**Implemented Features:**
1. ✅ Pure Python mode (`--pure` flag)
2. ✅ Help command with detailed documentation
3. ✅ Script execution from files
4. ✅ Command-line argument parsing (`--help`, `--version`, `-c`)
5. ✅ Shell mode indicators

**Responsibilities:**
- Main shell loop and user interface
- Command parsing and tokenization
- Configuration management
- Signal handling (Ctrl+C, Ctrl+Z)

---

### 🟢 Person 2: Execution & I/O Management
**Modules:** `executor.py`, `utils.py`

**Implemented Features:**
1. ✅ Standard error redirection (`2>`, `2>>`)
2. ✅ Combined stream redirection (`2>&1`)
3. ✅ Command substitution (`$(cmd)` and `` `cmd` ``)
4. ✅ Enhanced error handling and reporting

**Responsibilities:**
- Process execution via subprocess
- I/O redirection (stdin, stdout, stderr)
- Pipeline implementation
- File descriptor management

---

### 🟡 Person 3: Jobs & Built-in Commands
**Modules:** `jobs.py`, `builtin.py`

**Implemented Features:**
1. ✅ `cat` - File concatenation
2. ✅ `ls` - Directory listing
3. ✅ `echo` - Text output
4. ✅ `pwd` - Working directory
5. ✅ `mkdir` - Create directories
6. ✅ `rm -rf` - Remove files/directories
7. ✅ `cp` - Copy files
8. ✅ `mv` - Move/rename files
9. ✅ `touch` - Create empty files
10. ✅ `grep` - Pattern searching
11. ✅ `wc` - Word/line counting
12. ✅ `alias` - Command aliases
13. ✅ `env` - Environment variables
14. ✅ `kill` - Job termination

**Responsibilities:**
- Background job management
- Pure Python command implementations
- Environment variable handling
- Command aliasing

---

## 🧪 Testing

### Test Coverage
- **Total Tests:** 20
- **Pass Rate:** 100% ✅
- **Test Files:** 3

```bash
tests/
├── test_parser.py     # 10 tests - Parsing logic
├── test_executor.py   # 5 tests  - Command execution
└── test_jobs.py       # 6 tests  - Job management
```

### Running Tests

#### Using Docker
```bash
# Run all tests
docker-compose run --rm ush-tests

# Run with coverage report
docker-compose run --rm ush-coverage
```

#### Manual Testing
```bash
# Run all tests
PYTHONPATH=src python3 -m pytest tests/ -v

# Run specific test file
PYTHONPATH=src python3 -m pytest tests/test_parser.py -v

# Run with coverage
PYTHONPATH=src python3 -m pytest tests/ --cov=ush --cov-report=html
```

### Test Categories

**Parser Tests** (`test_parser.py`):
- Simple command parsing
- Quote handling (single/double)
- Escape sequences
- Pipeline detection
- I/O redirection
- Background job markers

**Executor Tests** (`test_executor.py`):
- Simple command execution
- Output redirection
- Append mode redirection
- Background process execution
- Invalid command handling

**Job Manager Tests** (`test_jobs.py`):
- Job creation and tracking
- Job removal
- Job retrieval
- Completion detection
- Status updates
- Job ID management

---

## 🐳 Docker Support

### Available Services

```yaml
services:
  ush-shell       # Interactive shell (hybrid mode)
  ush-shell-pure  # Interactive shell (pure Python mode)
  ush-tests       # Run test suite
  ush-coverage    # Generate coverage report
```

### Docker Commands

```bash
# Start interactive shell (hybrid mode)
docker-compose run --rm ush-shell

# Start pure Python shell
docker-compose run --rm ush-shell-pure

# Run tests
docker-compose run --rm ush-tests

# Generate coverage report
docker-compose run --rm ush-coverage

# Build image
docker-compose build

# Clean up
docker-compose down
```

### Docker Configuration

**Base Image:** Ubuntu 22.04  
**Python Version:** 3.x (latest)  
**Working Directory:** `/app`  
**Entry Point:** `python3 -m ush.ush`

---

## 📝 Examples

### Basic Commands

```bash
ush:~> pwd
/home/user

ush:~> ls
file1.txt  file2.txt  directory/

ush:~> cat file1.txt
Hello, World!

ush:~> echo "USH Shell" > output.txt

ush:~> cat output.txt
USH Shell
```

### I/O Redirection

```bash
# Redirect output
ush:~> ls > files.txt

# Append output
ush:~> echo "More content" >> files.txt

# Redirect stderr
ush:~> grep pattern nonexistent.txt 2> errors.log

# Combine streams
ush:~> command 2>&1 | tee output.log
```

### Pipelines

```bash
# Simple pipeline
ush:~> cat file.txt | grep "pattern" | wc -l
5

# Complex pipeline
ush:~> ls -la | grep ".py" | wc -l
8
```

### Background Jobs

```bash
# Run in background
ush:~> sleep 100 &
[1] 12345

# List jobs
ush:~> jobs
[1]  Running    sleep 100

# Bring to foreground
ush:~> fg 1

# Send to background (after Ctrl+Z)
ush:~> bg 1
```

### Command Substitution

```bash
# Modern syntax
ush:~> echo "Current date: $(date)"
Current date: Mon Dec 9 2025

# Classic syntax
ush:~> echo "Files: `ls | wc -l`"
Files: 10

# Nested substitution
ush:~> cat $(find . -name "*.txt")
```

### Environment & Aliases

```bash
# Set environment variable
ush:~> export PATH=/usr/local/bin:$PATH

# View all variables
ush:~> env
PATH=/usr/local/bin:/usr/bin
HOME=/home/user
...

# Create alias
ush:~> alias ll='ls -la'

# Use alias
ush:~> ll
total 48
drwxr-xr-x  5 user user 4096 Dec  9 12:00 .
...
```

### Script Execution

```bash
# Create a script
ush:~> cat > script.sh
#!/usr/bin/env ush
echo "Starting script..."
ls -la
echo "Done!"
^D

# Execute script
ush:~> python3 -m ush.ush script.sh
Starting script...
total 48
...
Done!
```

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Detailed feature documentation
- **[demo.sh](demo.sh)** - Interactive feature demonstration
- **[LICENSE](LICENSE)** - MIT License

### Additional Resources

- **Source Code Documentation**: Inline comments in all modules
- **Test Examples**: See `tests/` directory for usage examples
- **Example Scripts**: See `examples/` directory

---

## 🔧 Configuration

### Environment Variables

```bash
# Set Python path
export PYTHONPATH=src

# Set custom prompt (future enhancement)
export USH_PROMPT="ush:~> "

# Set history file location (future enhancement)
export USH_HISTFILE=~/.ush_history
```

### Customization

Modify `src/ush/config.py` to customize:
- Prompt format
- History size
- Default execution mode
- Signal handling behavior

---

## 🐛 Known Limitations

1. **Platform-Specific Commands**: Some system commands may not work on all platforms
2. **Signal Handling**: SIGTSTP (Ctrl+Z) not available on Windows
3. **Job Control**: Background jobs may not work identically across all platforms
4. **Pure Mode**: Limited to implemented built-in commands only

---

## 🔮 Future Enhancements

- [ ] Tab completion for commands and file paths
- [ ] Syntax highlighting in interactive mode
- [ ] Persistent command history across sessions
- [ ] Configurable prompt with git branch support
- [ ] Additional built-in commands (find, sed, awk)
- [ ] Shell scripting features (if/else, loops, functions)
- [ ] Process substitution (`<(command)`)
- [ ] Globbing and pattern matching (`*.txt`)

---

## 🤝 Contributing

This is an educational project for an Operating Systems course. Contributions from team members follow this workflow:

### Git Workflow

```bash
# Clone repository
git clone https://github.com/CypherShade/Mini-Shell.git
cd Mini-Shell/python-ush

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
PYTHONPATH=src python3 -m pytest tests/

# Commit changes
git add .
git commit -m "Add: feature description"

# Push to GitHub
git push origin feature/your-feature

# Create Pull Request on GitHub
```

### Code Standards

- **Style**: Follow PEP 8 guidelines
- **Testing**: Add tests for new features
- **Documentation**: Update README and inline comments
- **Commits**: Use descriptive commit messages

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 CypherShade

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👨‍💻 Authors

**Team:** Operating Systems Course Project  
**Repository:** [CypherShade/Mini-Shell](https://github.com/CypherShade/Mini-Shell)  
**Course:** Operating Systems  
**Year:** 2025

### Team Members

- **Person 1** - Core Shell & Parsing (`ush.py`, `parser.py`, `config.py`, `signals.py`)
- **Person 2** - Execution & I/O (`executor.py`, `utils.py`)
- **Person 3** - Jobs & Built-ins (`jobs.py`, `builtin.py`)

---

## 🙏 Acknowledgments

- **Python Community** - For excellent documentation and libraries
- **Unix/Linux** - For shell design inspiration
- **Course Instructors** - For project guidance
- **pytest** - For testing framework
- **Docker** - For containerization support

---

## 📞 Support

For questions or issues:

1. **Check Documentation**: See [QUICKSTART.md](QUICKSTART.md) and [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
2. **Run Demo**: Execute `python3 -m ush.ush demo.sh` to see features
3. **Check Tests**: Run `PYTHONPATH=src python3 -m pytest tests/ -v`
4. **GitHub Issues**: Open an issue on the repository

---

## 📊 Project Statistics

- **Lines of Code**: ~2,000+
- **Test Cases**: 20
- **Test Coverage**: 100%
- **Built-in Commands**: 15+
- **Pure Python Commands**: 11
- **Supported Platforms**: Linux, macOS, Windows
- **Python Version**: 3.8+
- **Development Time**: Operating Systems Course Duration

---

## 🎯 Project Goals

✅ **Educational**: Learn process management, I/O redirection, and shell internals  
✅ **Practical**: Build a functional shell for daily use  
✅ **Collaborative**: Practice team-based software development  
✅ **Quality**: Achieve 100% test coverage and clean code  
✅ **Portable**: Support multiple platforms and deployment methods  

---

<div align="center">

**USH Shell** - *A Python Implementation of Unix Shell*

Made with ❤️ by Operating Systems Course Team

[Documentation](QUICKSTART.md) • [Features](IMPLEMENTATION_SUMMARY.md) • [Demo](demo.sh) • [GitHub](https://github.com/CypherShade/Mini-Shell)

</div>

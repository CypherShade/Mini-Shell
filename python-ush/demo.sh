#!/usr/bin/env python3
# Demo script for USH Shell
# Run: python3 -m ush.ush demo.sh

echo "====================================="
echo "  USH Shell Feature Demonstration"
echo "====================================="
echo ""

# Basic commands
echo "1. Basic Commands:"
echo "Current directory:"
pwd
echo ""

# File operations
echo "2. File Operations:"
mkdir test_demo
cd test_demo
echo "Created test directory"
touch file1.txt file2.txt file3.txt
echo "Creating files..." > file1.txt
echo "Testing USH shell" > file2.txt
ls
echo ""

# I/O Redirection
echo "3. I/O Redirection:"
echo "Hello, World!" > output.txt
echo "Appending text..." >> output.txt
cat output.txt
echo ""

# Pipelines
echo "4. Pipelines:"
cat output.txt | grep "Hello"
echo ""

# Environment variables
echo "5. Environment Variables:"
export TEST_VAR="Hello from USH"
env | grep TEST_VAR
echo ""

# Clean up
echo "6. Cleanup:"
cd ..
rm -rf test_demo
echo "Demo complete!"
echo ""
echo "Try these commands yourself:"
echo "  - help           (show all commands)"
echo "  - jobs &         (background jobs)"
echo "  - alias          (create shortcuts)"
echo "====================================="

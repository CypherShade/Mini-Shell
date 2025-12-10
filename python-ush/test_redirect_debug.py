#!/usr/bin/env python3
"""Debug script to test file redirection"""

import os
import sys
import subprocess

# Add src to path
sys.path.insert(0, 'src')

from ush.executor import execute_command, set_job_manager
from ush.jobs import JobManager

# First, test subprocess.run directly
print("=" * 50)
print("Testing subprocess.run directly...")
with open('direct_test.txt', 'w') as f:
    result = subprocess.run(['echo', 'Direct test'], stdout=f)
print(f"Direct test file exists: {os.path.exists('direct_test.txt')}")
if os.path.exists('direct_test.txt'):
    with open('direct_test.txt', 'r') as f:
        print(f"Direct test content: {repr(f.read())}")
    os.remove('direct_test.txt')
print("=" * 50)

# Set up job manager
job_manager = JobManager()
set_job_manager(job_manager)

print(f"Current working directory: {os.getcwd()}")
print(f"Platform: {sys.platform}")

# Test command
command_structure = {
    'command': 'echo',
    'args': ['Redirected Output'],
    'redirects': [('>', 'test_output.txt')],
    'background': False
}

print("\nExecuting command...")
result = execute_command(command_structure)
print(f"Command result: {result}")

print(f"\nChecking for file...")
print(f"File exists: {os.path.exists('test_output.txt')}")

if os.path.exists('test_output.txt'):
    with open('test_output.txt', 'r') as f:
        content = f.read()
    print(f"File content: {repr(content)}")
    os.remove('test_output.txt')
else:
    print("Listing files in current directory:")
    print(os.listdir('.'))

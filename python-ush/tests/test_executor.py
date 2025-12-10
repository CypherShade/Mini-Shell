import unittest
import os
from ush.executor import execute_command, set_job_manager
from ush.jobs import JobManager

class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.job_manager = JobManager()
        set_job_manager(self.job_manager)

    def test_simple_command(self):
        # Test command with structured input
        import sys
        if sys.platform == 'win32':
            # Use a Windows command
            command_structure = {
                'command': 'cmd',
                'args': ['/c', 'echo', 'Hello World'],
                'redirects': [],
                'background': False
            }
        else:
            command_structure = {
                'command': 'echo',
                'args': ['Hello', 'World'],
                'redirects': [],
                'background': False
            }
        result = execute_command(command_structure)
        self.assertEqual(result, 0)  # Success exit code

    def test_command_with_redirection(self):
        # Test redirection to file
        import sys
        test_file = 'test_output.txt'
        try:
            if sys.platform == 'win32':
                command_structure = {
                    'command': 'cmd',
                    'args': ['/c', 'echo', 'Redirected Output'],
                    'redirects': [('>', test_file)],
                    'background': False
                }
            else:
                command_structure = {
                    'command': 'echo',
                    'args': ['Redirected Output'],
                    'redirects': [('>', test_file)],
                    'background': False
                }
            execute_command(command_structure)
            
            # Verify the file was created and contains the output
            self.assertTrue(os.path.exists(test_file))
            with open(test_file, 'r') as f:
                output = f.read()
            self.assertIn('Redirected', output)
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_background_job(self):
        # Test background job execution
        command_structure = {
            'command': 'ping',
            'args': ['localhost', '-n', '2'] if os.name == 'nt' else ['localhost', '-c', '2'],
            'redirects': [],
            'background': True
        }
        result = execute_command(command_structure)
        # Background jobs return PID, which should be an integer
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_invalid_command(self):
        # Test invalid command handling
        command_structure = {
            'command': 'invalid_command_xyz123',
            'args': [],
            'redirects': [],
            'background': False
        }
        result = execute_command(command_structure)
        self.assertEqual(result, 127)  # Command not found exit code
    
    def test_append_redirection(self):
        # Test append redirection
        import sys
        test_file = 'test_append.txt'
        try:
            if sys.platform == 'win32':
                command_structure1 = {
                    'command': 'cmd',
                    'args': ['/c', 'echo', 'First line'],
                    'redirects': [('>', test_file)],
                    'background': False
                }
                command_structure2 = {
                    'command': 'cmd',
                    'args': ['/c', 'echo', 'Second line'],
                    'redirects': [('>>', test_file)],
                    'background': False
                }
            else:
                command_structure1 = {
                    'command': 'echo',
                    'args': ['First line'],
                    'redirects': [('>', test_file)],
                    'background': False
                }
                command_structure2 = {
                    'command': 'echo',
                    'args': ['Second line'],
                    'redirects': [('>>', test_file)],
                    'background': False
                }
            execute_command(command_structure1)
            execute_command(command_structure2)
            
            self.assertTrue(os.path.exists(test_file))
            with open(test_file, 'r') as f:
                content = f.read()
            self.assertIn('First', content)
            self.assertIn('Second', content)
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
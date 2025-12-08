import unittest
import shlex
from ush.parser import parse_command, tokenize_command

class TestParser(unittest.TestCase):

    def test_simple_command(self):
        command = "ls -l"
        result = parse_command(command)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'ls')
        self.assertEqual(result[0]['args'], ['-l'])
        self.assertEqual(result[0]['background'], False)

    def test_command_with_quotes(self):
        command = 'echo "Hello, World!"'
        result = parse_command(command)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'echo')
        self.assertEqual(result[0]['args'], ['Hello, World!'])

    def test_command_with_escape(self):
        command = "echo Hello\\ World"
        result = parse_command(command)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'echo')
        self.assertEqual(result[0]['args'], ['Hello World'])

    def test_command_with_multiple_arguments(self):
        command = "cp file1.txt file2.txt"
        result = parse_command(command)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'cp')
        self.assertEqual(result[0]['args'], ['file1.txt', 'file2.txt'])

    def test_command_with_pipe(self):
        # Pipes are now parsed into separate commands
        command = "cat file.txt | grep 'search_term'"
        result = parse_command(command)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['command'], 'cat')
        self.assertEqual(result[0]['args'], ['file.txt'])
        self.assertEqual(result[1]['command'], 'grep')
        self.assertEqual(result[1]['args'], ['search_term'])
        self.assertTrue(result[0].get('is_pipeline', False))
        self.assertTrue(result[1].get('is_pipeline', False))

    def test_command_with_redirection(self):
        command = "command > output.txt"
        result = parse_command(command)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'command')
        self.assertEqual(result[0]['redirects'], [('>', 'output.txt')])

    def test_empty_command(self):
        command = ""
        expected = []
        self.assertEqual(parse_command(command), expected)
    
    def test_background_command(self):
        command = "sleep 10 &"
        result = parse_command(command)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'sleep')
        self.assertEqual(result[0]['args'], ['10'])
        self.assertEqual(result[0]['background'], True)
    
    def test_tokenize_command(self):
        command = "ls -l"
        expected = ["ls", "-l"]
        self.assertEqual(tokenize_command(command), expected)

if __name__ == '__main__':
    unittest.main()
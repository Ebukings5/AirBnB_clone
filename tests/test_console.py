import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):

    def setUp(self):
        """Set up for test."""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down after test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def capture_stdout(self, command):
        """Capture stdout output."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(command)
            return f.getvalue()

    def test_all_command(self):
        """Test 'all' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("State.all()")
            output = f.getvalue().strip()
            self.assertIn("State", output)

    def test_count_command(self):
        """Test 'count' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("City.count()")
            output = f.getvalue().strip()
            self.assertEqual(output, "0")

    def test_show_command(self):
        """Test 'show' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.show(12345)")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_destroy_command(self):
        """Test 'destroy' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("Place.destroy(12345)")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_update_command_single_attribute(self):
        """Test 'update' command with single attribute."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('User.update("12345", "first_name", "John")')
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_update_command_dictionary(self):
        """Test 'update' command with dictionary."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('User.update("12345", {"first_name": "John", "age": 30})')
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_invalid_command(self):
        """Test invalid command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("InvalidCommand()")
            output = f.getvalue().strip()
            self.assertIn("name 'InvalidCommand' is not defined", output)

    def test_syntax_error(self):
        """Test syntax error."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.update()")
            output = f.getvalue().strip()
            self.assertIn("Usage: User.update(<id>, <attribute name>, <attribute value>)", output)

    def test_quit_command(self):
        """Test 'quit' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))

    def test_EOF_command(self):
        """Test 'EOF' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))

if __name__ == "__main__":
    unittest.main()
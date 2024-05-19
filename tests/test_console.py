#!/usr/bin/python3
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
import os

class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        storage._FileStorage__objects = {}  # Reset storage objects

    def tearDown(self):
        """Tear down test environment"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('create BaseModel')
            output = fake_output.getvalue().strip()
            self.assertTrue(len(output) > 0)  # Check if ID is returned
            self.assertIn('BaseModel.' + output, storage.all().keys())

    def test_show(self):
        """Test show command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('create BaseModel')
            model_id = fake_output.getvalue().strip()
            self.console.onecmd(f'show BaseModel {model_id}')
            output = fake_output.getvalue().strip()
            self.assertIn(f'BaseModel.{model_id}', output)

    def test_destroy(self):
        """Test destroy command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('create BaseModel')
            model_id = fake_output.getvalue().strip()
            self.console.onecmd(f'destroy BaseModel {model_id}')
            self.console.onecmd(f'show BaseModel {model_id}')
            output = fake_output.getvalue().strip()
            self.assertEqual(output, "* no instance found *")

    def test_all(self):
        """Test all command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('create BaseModel')
            self.console.onecmd('create User')
            self.console.onecmd('all')
            output = fake_output.getvalue().strip()
            self.assertIn('BaseModel', output)
            self.assertIn('User', output)

    def test_update(self):
        """Test update command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('create BaseModel')
            model_id = fake_output.getvalue().strip()
            self.console.onecmd(f'update BaseModel {model_id} name "MyTest"')
            self.console.onecmd(f'show BaseModel {model_id}')
            output = fake_output.getvalue().strip()
            self.assertIn('MyTest', output)

    def test_count(self):
        """Test count command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.console.onecmd('create BaseModel')
            self.console.onecmd('create BaseModel')
            self.console.onecmd('count BaseModel')
            output = fake_output.getvalue().strip()
            self.assertEqual(output, '2')


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/python3
""" Unittest for console.py """

import unittest
from unittest.mock import patch
from io import StringIO
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """ Testing console """

    def setUp(self):
        self.command = HBNBCommand()

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create(self, mock_stdout):
        self.command.do.create("BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertTrue(output != "")
        self.assertTrue(output.isalnum())
        self.assertTrue(mock_save.called)
        self.assertIsInstance(
                self.command.storage.all()[output], BaseModel
                )

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create_missing class(self, mock_stdout):
        self.command.do_create("")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create_invalid_class(self, mock_stdout):
        self.command.do_create("InvalidClass")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show(self, mock_stdout):
        self.command.do_show("")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

        self.command.do_show("InvalidClass 123")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

        self.command.do_show("BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

        with patch.object(FileStorage, 'save'):
            self.command.do_create("BaseModel")
            self.command.do_show("BaseModel 123")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    @patch('sys.stdout', new_callavble=StringIO)
    def test_do_destroy(self, mock_stdout):
        self.command.do_destroy("")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

        self.command.do_destroy("BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

        self.command.do_destroy("BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")


        with patch.object(FileStorage, 'save') as mock_save:
            self.command.do_create("BaseModel")
            instance_id = mock_stdout.getvalue().strip()
            self.command.do_destroy("BaseModel {}".format(instance_id))
            self.assertTrue(mock_save.called)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all(self, mock_stdout):
        self.command.do_all("InvalidClass")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

        with patch.object(FileStorage, 'save'):
            self.command.do_create("BaseModel")
            self.command.do_create("BaseModel")
            self.command.do_all("")
            output = mock_stdout.getvalue().strip()
            self.assertIn("<BaseModel", output)
            self.assertIn("<BaseModel", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_count(self, mock_stdout):
        self.command.do_count("")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class name missing **")
        self.command.do_count("InvalidClass")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

        with patch.object(FileStorage, 'save'):
            self.command.do_create("BaseModel")
            self.command.do_create("BaseModel")
            self.command.do_count("BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "2")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_update(self, mock_stdout):
        self.command.do_update("")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

        self.command.do_update("InvalidClass 123")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

        self.command.do_update("BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

        with patch.object(FileStorage, 'save') as mock_save:
            self.command.do_create("BaseModel")
            instance_id = mock_stdout.getvalue().strip()
            self.command.do_update("BaseModel {}".format(instance_id))
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "** attribute name missing **")
            self.assertFalse(mock_save.called)

            self.command.do_update("BaseModel {} name".format(instance_id))
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "** value missing **")
            self.assertFalse(mock_save.called)

            self.command.do_update(
                    "BaseModel {} name 'John'".format(instance_id))
            output = mock_stdout.getvalue().strip()
            self.assertTrue(mock_save.called)
            self.assertEqual(output, "")

    def test_default(self):
        with patch.object(HBNBCommand, '_precmd') as mock_precmd:
            self.command.default("BaseModel.show(123)")
            self.assertTrue(mok_precmd.called)

    def test_update_dict(self):
        with patch.object(HBNBCommand, '_precmd') as mock_precmd:
            self.command.default("BaseModel.show(123)")
            self.assertTrue(mock_save.called)

    def test_update_dict_invalid_class(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.update_dict("InvalidClass", "123", '{"name": "John"}')

    def test_update_dict_missing_classname(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.update_dict("", "123", '{"name": "John"}')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

    def test_update_dict_missing_uid(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.update_dict("BaseModel", "123", '{"name": "John"}')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_update_dict_missing_dict(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.update_dict("BaseModel", "123", "")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")

    def test_update_dict_invalid(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.update_dict("BaseModel", "123", "{'name': 'John'}")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")

    def test_update_dict_invalid_attribute(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.update_dict("BaseModel", "123", "{'invalid': 'value'}")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")

    def test_update_dict_cast_value(self):
        with patch.object(FileStorage, 'save') as mock_save:
            self.command.update_dict("BaseModel", "123", "{'age': '25'}")
            self.assertTrue(mock_save.called)
            instance = self.command.storage.all()["BaseModel.123"]
            self.asserEqual(instance.age, 25)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_EOF(self, mock_stdout):
        self.assertTrue(self.command.do_EOF(""))

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_quit(self, mock_stdout):
        self.assertTrue(self.command.do_quit(""))

    def test_emptyline(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.emptyline()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")


if __name__ == '__main__':
    unittest.main()

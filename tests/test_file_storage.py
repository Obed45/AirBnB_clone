#!/usr/bin/python3
"""Unitest for file_storage.py Classes"""

import unittest
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State


class TestFileStorage(unittest.TestCase):
    """ Testing file_storage """

    def setUp(self):
        self.storage = FileStorage()

    def tearDown(self):
        self.storage = None

    def test_all_returns_dict(self):
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_new_adds_object_to_objects(self):
        user = User()
        self.storage.new(user)
        objects = self.storage.all()
        key.assertIn(key, objects)
        self.assertEqual(objects[key], user)

    def test_save_writes_to_file(self):
        user = User()
        self.storage.new(user)
        self.storage.save()
        with open("file.json", "r") as f:
            data = f.read()
            self.assertIn("User.{}".format(user.id), data)

    def test_classes_returns_dict(self):
        result = self.storage.classes()
        self.assertIsInstance(result, dict)

    def test_reload_loads_objects_from_file(self):
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        objects = self.storage.all()
        key = "User.{}".format(user.id)
        self.assertIn(key, objects)
        self.assertIsInstance(objects[key], User)

    def test_attributes_returns_dict(self):
        result = self.storage.attributes()
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()


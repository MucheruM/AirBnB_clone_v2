#!/usr/bin/python3

"""This module tests the DBStorage class."""

import os
import unittest
from models import storage
from models.engine.db_storage import DBStorage
from models.state import State


storage_type = os.getenv("HBNB_TYPE_STORAGE")
env = os.getenv("HBNB_ENV")


@unittest.skipIf(storage_type != "db" and env != "test", "Skipping file tests")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorge class"""

    def setUp(self):
        """Set up for the test"""
        storage.rollback()
        storage.drop_all()
        storage.reload()

    def test_is_instance(self):
        """Test if storage is an instance of the BDStorage class"""
        self.assertIsInstance(storage, DBStorage)

    def test_all(self):
        """Test if `all` func returns the dictionary"""
        obj = storage.all()
        self.assertIsInstance(obj, dict)
        self.assertTrue(len(obj) == 0)

    def test_new(self):
        """Test if `new` func adds an obj to the dbase"""
        state = State(name="LosAngeles")
        storage.new(state)
        self.assertIn(state, storage.all().values())

    def test_save(self):
        """Test if `save` func commits all changes to db"""        state = State(name="LosAngeles")
        storage.new(state)
        storage.save()
        self.assertIn(state, storage.all().values())

    def test_delete(self):
        """Test if `delete` clears and obj from the db"""
        state = State(name="LosAngeles")
        storage.new(state)
        storage.save()
        storage.delete(state)
        self.assertNotIn(state, storage.all().values())

    def test_reload(self):
        """Test if `reload`reloads all tables in the db"""
        state = State(name="LosAngeles")
        storage.new(state)
        storage.save()
        storage.reload()
        self.assertNotIn(state, storage.all().values())

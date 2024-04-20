#!/usr/bin/python3
"""The module tests the BaseModel class"""

import os
import unittest
import datetime
from uuid import UUID
import json


class test_basemodel(unittest.TestCase):
    """The class to be tested"""

    def __init__(self, *args, **kwargs):
        """The init function the gives all self same attr"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel


    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """Tests the BaseModel"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Tests the func attr of the class"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test the int arg in the class att"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "file")        
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ Testing the string arg in the BaseModel class"""
        i = self.value()
        dictionary = i.get_dict_without_sa_instance()
        self.assertEqual(
            str(i), f"[{self.name}] ({i.id}) {dictionary}"
        )

    def test_to_dict(self):
        """ Test the `to_dict` method in the BaseModel class"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test arg with None keyword arg"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ Test instantiation with one kwarg"""
        n = {'name': 'test'}
        instance = self.value(**n)
        
        self.assertIn("name", instance.__dict__)
        self.assertIn("test", instance.__dict__.values())
        
    def test_id(self):
        """Test the id in the class """
        new = self.value()
        self.assertEqual(type(new.id), str)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "file")
    def test_created_at(self):
        """Test the `created_at`attr in the BaseModel"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "file")
    def test_updated_at(self):
        """Test the update at attr in the BaseModel class"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        new.save()
        self.assertFalse(new.created_at == new.updated_at)

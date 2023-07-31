#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import unittest

import pep8

import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.engine import db_storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipUnless(models.storage_t == 'db', "test only db storage")
    def test_get(self):
        """retrieve an object based on the class and its id"""
        state = State(name="Kenya")
        state.save()
        city = City(name="Nairobi", state_id=state.id)
        city.save()

        result = storage.get(State, state.id)
        self.assertEqual(state.id, result.id)

        result = storage.get(City, city.id)
        self.assertEqual(city.id, result.id)
        self.assertEqual(city.state_id, state.id)

    @unittest.skipUnless(models.storage_t == 'db', "test only db storage")
    def test_count(self):
        """count number of objects in storage"""
        initial_objs = storage.count()
        initial_states = storage.count(State)
        state = State(name="Uganda")
        state.save()
        total_objs = storage.count()
        total_states = storage.count(State)

        self.assertIsInstance(initial_objs, int, "count should be integer")
        self.assertIsInstance(initial_states, int, "count should be integer")
        self.assertIsInstance(total_objs, int, "count should be integer")
        self.assertIsInstance(total_states, int, "count should be integer")
        self.assertEqual(total_objs, initial_objs + 1)
        self.assertEqual(total_states, initial_states + 1)
        self.assertGreater(total_objs, initial_objs)
        self.assertGreater(total_states, initial_states)

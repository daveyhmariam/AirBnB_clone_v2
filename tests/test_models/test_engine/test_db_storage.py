#!/usr/bin/python3
import unittest
import MySQLdb
from os import getenv
from models.engine.db_storage\
import DBStorage
from models.state import State
from models.city import City


class Test_db_storage(unittest.TestCase):
    '''testing database storage functions'''

    def setUp(self) -> None:
        self.conn = MySQLdb.connect(
            host=getenv('HBNB_MYSQL_HOST'),
            user=getenv('HBNB_MYSQL_USER'),
            passwd=getenv('HBNB_MYSQL_PWD'),
            database=getenv('HBNB_MYSQL_DB')
        )
        self.cursor = self.conn.cursor()
        self.storage = DBStorage()
        self.storage.reload()
    
    def tearDown(self) -> None:
        self.cursor.close()
        self.conn.close()

    def test_empty(self):
        self.assertEqual(len(self.storage.all()), 0)

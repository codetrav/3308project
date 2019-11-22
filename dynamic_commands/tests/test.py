import sys
sys.path.insert(
    0, "/home/willwalker/OneDrive/2019/Fall 2019/CSCI 3308/Project/Git/3308project/dynamic_commands")

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import main
from smartOBD import test_commands
from smartOBD import dbconnect
from smartOBD import asynco
from io import StringIO
import psycopg2
import smartOBD
import pytest

class TestClass2():
    def test_getAsync(self, monkeypatch):
        monkeypatch.setattr('sys.stdin', open(
            '/home/willwalker/OneDrive/2019/Fall 2019/CSCI 3308/Project/Git/my3308project/dynamic_commands/tests/inputs.txt'))
        asynco.getAsync(10)

    def test_db_assert(self):
        assert type(dbconnect.dbconn) is psycopg2._ext.connection
        assert type(dbconnect.cur) is psycopg2._ext.cursor

    def test_fullQuery(self, monkeypatch):
        monkeypatch.setattr('sys.stdin', open(
            '/home/willwalker/OneDrive/2019/Fall 2019/CSCI 3308/Project/Git/my3308project/dynamic_commands/tests/inputs.txt'))
        test_commands.fullQuery()
stdin = sys.stdin
main_input0 = StringIO('0')
main_input1 = StringIO('1\nwalkerwg\nmini\njcw')


class TestClass(unittest.TestCase):
    @patch('smartOBD.asynco.getAsync')
    def test_getAsyncCall(self, mock):
        sys.stdin = main_input0
        main.main()
        self.assertTrue(mock.called)
    
    @patch('smartOBD.test_commands.fullQuery')
    def test_fullQueryCall(self,mock):
        sys.stdin = main_input1
        main.main()
        self.assertTrue(mock.called)


if __name__ == "__main__":
    unittest.main()

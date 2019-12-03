import sys,os
sys.path.insert(
    0, os.path.realpath(os.path.dirname(__file__)+"/.."))

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from smartOBD import main
from smartOBD import test_commands
from smartOBD import dbconnect
from smartOBD import asynco
from io import StringIO
import psycopg2
import smartOBD
import pytest

test_singlecar = StringIO('codehawk\n')
test_multicar = StringIO('walkerwg\nmini\njcw\n')
main_input1 = StringIO('0')
test_failcar = StringIO('walkerwg\nj\na\n')
class TestClass2():
    def test_getAsync(self):
        test_multicar = StringIO('walkerwg\nmini\njcw\n')
        sys.stdin = test_multicar
        asynco.getAsync(10)

    def test_db_assert(self):
        assert type(dbconnect.dbconn) is psycopg2._ext.connection
        assert type(dbconnect.cur) is psycopg2._ext.cursor

    def test_fullQuery(self):
        test_multicar = StringIO('walkerwg\nmini\njcw\n')
        sys.stdin = test_multicar
        test_commands.fullQuery()

    def test_failed_username(self):
        main_input1 = StringIO('0')
        sys.stdin = main_input1
        with pytest.raises(SystemExit):
            test_commands.fullQuery()
        main_input1 = StringIO('0')
        sys.stdin = main_input1
        with pytest.raises(SystemExit):
            asynco.getAsync(60)
    
    def test_failed_car(self):
        test_failcar = StringIO('walkerwg\nj\na\n')
        sys.stdin = test_failcar
        with pytest.raises(SystemExit):
            test_commands.fullQuery()
        test_failcar = StringIO('walkerwg\nj\na\n')
        sys.stdin = test_failcar
        with pytest.raises(SystemExit):
            asynco.getAsync(60)
    
    def test_assert_multi_car(self,capsys):
        sys.stdin = test_multicar
        test_commands.fullQuery()
        captured = capsys.readouterr()
        assert captured.out == 'Please input your username from the website so we can upload your information to your account: Looks like you have more than one car, which car would you like to access?\n\nMake: Model: Failed OBD-II Query, please try again\n'
        
    def test_single_car(self,capsys):
        sys.stdin = test_singlecar
        test_commands.fullQuery()
        captured = capsys.readouterr()
        assert captured.out == 'Please input your username from the website so we can upload your information to your account: Failed OBD-II Query, please try again\n'

stdin = sys.stdin
main_input0 = StringIO('0')
main_input = StringIO('1\nwalkerwg\nmini\njcw')


class TestClass(unittest.TestCase):
    @patch('smartOBD.asynco.getAsync')
    def test_getAsyncCall(self, mock):
        sys.stdin = main_input0
        main.main()
        self.assertTrue(mock.called)
    
    @patch('smartOBD.test_commands.fullQuery')
    def test_fullQueryCall(self,mock):
        sys.stdin = main_input
        main.main()
        self.assertTrue(mock.called)


if __name__ == "__main__":
    unittest.main()

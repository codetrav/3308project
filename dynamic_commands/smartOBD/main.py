"""
.. module:: main
   :platform: Unix
   :synopsis: Asynchronous connection

.. moduleauthor:: Will Walker

Initialization and interface
Simple command line interface, with choices for asynchronous data and a full data query

"""
import sys,os
sys.path.insert(
    0, os.path.realpath(os.path.dirname(__file__)))
import obd
import time
import psycopg2
import datetime
from psycopg2.extensions import AsIs
from psycopg2 import sql
import smartOBD
from smartOBD import asynco
from smartOBD import test_commands

##main function
# 
# initialization and interface for smartOBD
# Simple command line interface, with choices for asynchronous data and a full data query
def main():
    """ 
    This function determines which functionality the user would like to use, and calls it
    """
    print("Welcome to smartOBD")
    print("Choose your action:\n")
    print("(0) Async allows smartOBD to give you live data on your vehicle\n")
    print("(1) Full Read will store all the data from your car's computer\n")
    choose_action = input("Async(0) or Full Read(1): ")
    # * make database connection
    # host=198.23.146.166  password=Sweden77
    ## asynchronous
    # @param choose_action The action
    if(choose_action == '0'):
        asynco.getAsync(60)
        
        # x = 0
        # while x < 30:
        #     data = [datetime.datetime.now()]
        #     asynco.new_speed(x+3, data)
        #     asynco.new_rpm(1000+x, data)
        #     asynco.new_temp(150+x, data)
        #     asynco.new_fuel(35+x, data, dbtable, dbconn, cur)
        #     x += 1
    ## full query
    elif(choose_action == '1'):
        test_commands.fullQuery()
## constructor
if __name__ == "__main__":
    main()

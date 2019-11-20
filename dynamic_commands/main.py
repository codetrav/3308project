import smartOBD
import obd
import time
import psycopg2
import datetime
from psycopg2.extensions import AsIs
from psycopg2 import sql

##main function
# 
# initialization and interface for smartOBD
# Simple command line interface, with choices for asynchronous data and a full query

def main():
    print("Welcome to smartOBD")
    ##database connection
    dbconn = psycopg2.connect("host=198.23.146.166 dbname=car user=postgres")
    if(not dbconn):
        print("Database Connection Failed")
        exit()
    cur = dbconn.cursor()
    smartOBD.cur = cur
    smartOBD.dbconn = dbconn
    print("Choose your action:\n")
    print("(0) Async allows smartOBD to give you live data on your vehicle\n")
    print("(1) Full Read will store all the data from your car's computer\n")
    choose_action = input("Async(0) or Full Read(1): ")
    # * make database connection
    # host=198.23.146.166  password=Sweden77
    ## asynchronous
    # @param choose_action The action
    if(choose_action == '0'):
        smartOBD.getAsync(60)
        
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
        smartOBD.fullQuery()
    ## closing database connection
    if(dbconn):
        cur.close()
        dbconn.close()
        print("PostgreSQL connection is closed")

## constructor
if __name__ == "__main__":
    main()

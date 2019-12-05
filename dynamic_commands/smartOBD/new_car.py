import psycopg2
import string
import datetime
from psycopg2 import sql
from psycopg2.extensions import AsIs
from psycopg2.extensions import QuotedString
from .dbconnect import dbconn, cur, dbtable


def new_car():
    """
    Creates new car in database based on username. Collects make, model, model year for car and adds it to the cars table
    """
    print("Add new car to database")
    username = input("Please input your username: ")
    query = sql.SQL("SELECT id FROM users WHERE username = %s;")
    cur.execute(query, (username,))
    userid = cur.fetchone()
    if(userid == None):
        print("User not found, please try again")
        exit()
    make = input("Please input your car's make: ")
    model = input("Please input your car's model: ")
    year = input("Please input your car's model year: ")
    query = sql.SQL("INSERT into cars values (%s, %s, %s, %s)")
    cur.execute(query, (make, model, (year+"-01-01"), userid))
    query = sql.SQL(
        "select id from cars where model = %s AND make = %s AND owner=%s")
    cur.execute(query, (model.lower(), make.lower(), userid))
    car_id = cur.fetchone()
    if(car_id == None):
        print("Car not found, please try again")
        exit()
    car_id = int(car_id[0]) - 1
    query = sql.SQL("CREATE TABLE car%s (time timestamp);")
    cur.execute(query, (car_id,))
    query = sql.SQL("CREATE TABLE car%s_temp (time timestamp, SPEED_KMPH varchar(2000), RPM varchar(2000), Coolant_Temp varchar(2000), FUEL_LEVEL varchar(2000), MAF varchar(2000), Voltage varchar(2000));")
    cur.execute(query, (car_id,))
    dbconn.commit()
    if(dbconn):
        cur.close()
        dbconn.close()
        print("PostgreSQL connection is closed")

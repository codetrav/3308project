"""
.. module:: asynco
   :platform: Unix
   :synopsis: Asynchronous connection

.. moduleauthor:: Will Walker

Reads data using async functions and writes to a single row of the database to be read by the website

 """
from .dbconnect import cur, dbtable, dbconn
import obd
import time
import psycopg2
import datetime
from psycopg2.extensions import AsIs
from psycopg2 import sql
from obd import OBDStatus
# storage of data to be updated to the database
data = [datetime.datetime.now()]
obd.logger.removeHandler(obd.console_handler)


# User Get
#
# fetches car table and sets dbtable to carX_temp
# inputs: username
# sorts through database to find final car table
def userGet():
    """ This function gets the user and write the dbtable

    :param dbconn: The database connection class.
    :type dbconn: psycopg2 database connection
    :param cur: The cursor from the database.
    :type cur: psycopg2 database cursor
    :returns: name of car table (str).

    Writes dbtable name to global variable dbtable
    """
    username = input(
        "Please input your username from the website so we can upload your information to your account: ")
    username = str(username)
    query = sql.SQL("SELECT id FROM users WHERE username = %s;")
    cur.execute(query, (username,))
    userid = cur.fetchone()
    if(userid == None):
        print("Username not found, please try again")
        exit()
    userid = userid[0]
    if(username == 'codehawk'):
        userid = 0

    query = sql.SQL("select count(*) from cars where owner = %s;")
    cur.execute(query, str(userid))
    carcount = cur.fetchall()[0][0]
    if(carcount > 1):
        print(
            "Looks like you have more than one car, which car would you like to access?\n")
        car_make = input("Make: ")
        car_model = input("Model: ")
        query = sql.SQL(
            "select id from cars where model = %s AND make = %s AND owner=%s")
        cur.execute(query, (car_model.lower(), car_make.lower(), userid))
        car_id = cur.fetchone()
        if(car_id == None):
            print("Car not found, please try again")
            exit()
        car_id = int(car_id[0]) - 1
    else:
        cur.execute("select id from cars where owner = %s", str(userid))
        car_id = cur.fetchone()
        if(car_id == None):
            return ' '
        car_id = int(car_id[0]) - 1

    dbtable = "car"+str(car_id)+"_temp"
    return dbtable

# Write to Database
#
# erases data from database and writes updated values to database


def writeToDB():
    """ Writes to database
    Erases data from database and writes new values to be read by the website
    """
    # print("data is", data)
    cur.execute("delete from %s;", [AsIs(dbtable)])
    cur.execute(
        "insert into %s VALUES(%s, %s, %s, %s, %s, %s, %s);", (AsIs(dbtable), data[0], data[1], data[2], data[3], data[4], data[5]. data[6]))
    dbconn.commit()


# new_speed
#
# callback for speed writing to @data
def new_speed(s):
    data.clear()
    data.append(datetime.datetime.now())
    data.append(str(s.value))

# new_rpm
#
# callback for rpm writing to @data


def new_rpm(r):
    data.append(str(r.value))
    # print(r.value)

# new_temp
#
#  callback for coolant temperature writing to @data


def new_temp(t):
    data.append(str(t.value))

# new_temp
#
#  callback for fuel level writing to @data


def new_fuel(f):
    data.append(str(f.value))


def new_maf(m):
    data.append(str(m.value))


def new_volt(v):
    data.append(str(v.value))
    writeToDB(data, dbtable, dbconn, cur)


# getAsync
#
# sets connection for async, starts connection and waits for key entry to stop connection
def getAsync(dur):
    """ sets connection for async fucntions
    Starts connection and waits for key press to stop connection
    """
    dbtable = userGet()
    connection = obd.Async()
    if(connection.status() == OBDStatus.NOT_CONNECTED):
        print("Failed OBD-II Query, please try again")
    else:
        connection.watch(obd.commands.SPEED, callback=new_speed)
        connection.watch(obd.commands.RPM, callback=new_rpm)
        connection.watch(obd.commands.COOLANT_TEMP, callback=new_temp)
        connection.watch(obd.commands.MAF, callback=new_maf)
        connection.watch(obd.commands.CONTROL_MODULE_VOLTAGE,
                         callback=new_volt)
        connection.watch(obd.commands.FUEL_LEVEL, callback=new_fuel)

        connection.start()
        # the callback will now be fired upon receipt of new values
        if(connection.is_connected()):
            print("Successful Connection")
            input("Press any key to exit async...")
            connection.stop()
            cur.execute("delete from %s;", [AsIs(dbtable)])
            dbconn.commit()
            if(dbconn):
                cur.close()
                dbconn.close()
                print("PostgreSQL connection is closed")
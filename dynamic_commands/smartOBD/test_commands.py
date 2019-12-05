""" 
.. module:: fullQuery
   :platform: Unix
   :Synopsis: Full Query

.. moduleauthor:: Will Walker

Runs every compatible command to query as much data as possible from vehicle and writes to a new row in the database
"""
# \namespace test_commands
#
# Parsing through all OBDCommands as a dictionary, and then querying the car with all of them. \n
# Takes results, and writes them to database

import obd
import psycopg2
import string
import datetime
from obd import OBDStatus
from psycopg2 import sql
from psycopg2.extensions import AsIs
from psycopg2.extensions import QuotedString
from .dbconnect import cur, dbtable, dbconn
from tqdm import tqdm
from tqdm import trange
# obd.logger.setLevel(obd.logging.DEBUG)

# User Get
#
# fetches car table and sets dbtable to carX \n
# inputs: username \n
# sorts through database to find final car table


def userGet(dbconn, cur):
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

    dbtable = "car"+str(car_id)
    return dbtable


def fullQuery():
    """ 
    Gets dbtable name, then attempts connection with car.
    After connection is established, all commands are queried, and the successful ones are written to the database
    """
    dbtable = userGet(dbconn, cur)
    obd.logger.removeHandler(obd.console_handler)
    # * make car connection:
    car = obd.OBD()  # * auto-connects to USB or RF port
    command = []
    test_dict = obd.commands.__dict__
    if(car.status() == OBDStatus.NOT_CONNECTED):
        print("Failed OBD-II Query, please try again")
    else:
        # * column names
        columns = ["time"]
        # * column values
        results = [datetime.datetime.now()]
        # dictionary generation
        for key, i in tqdm(test_dict.items(), desc="Generating Dictionary"):
            # print(key, test_dict[key])
            command.append((key, test_dict[key]))
        # command = tuple(command)
        # print(command[0])
        with tqdm(desc="Querying Car", total=82) as pbar:
            temp2 = command[0][1][1]
            for i in range(3, 32):
                # print("Temp2 is", temp2[1][i])
                # print("Type is", type(temp2[1][i]))
                res = str((car.query(temp2[i])).value)
                # print('Passed query')
                description = str(temp2[i])
                # print(type(description))
                # print("Final command is")
                # print(description, res)
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(34, 64):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(66, len(temp2)):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()

            temp2 = command[0][1][6]
            for i in range(1, 32):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(33, 48):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(49, 64):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(65, 96):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(97, 128):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(129, 160):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
            for i in range(161, len(temp2)):
                res = str((car.query(temp2[i])).value)
                description = str(temp2[i])
                if(res != 'None'):
                    columns.append(description.rsplit(': ', 1)[1])
                    results.append(str(res).rsplit(' ', 1)[0])
                    pbar.update()
        pbar.close()
        # temp2 = command[0][1][9]
        # for i in range(0, len(temp2)):
        #     res = str((car.query(temp2[i])).value)
        #     description = str(temp2[i])
        #     if(res != 'None'):
        #         columns.append(description.rsplit(': ', 1)[1])
        #         results.append(str(res).rsplit(' ', 1)[0])
        # * length checking for all arrays
        if(len(columns) != len(results)):
            print("Results error")
        # *final loop for database access
        else:
            print("Parsing success")
            # * checking all columns for existence
            for i in trange(1, len(columns), desc="Sending to Database"):
                data = columns[i]
                data = data.replace("'", " ")
                data = data.replace("\"", " ")
                cur.execute("select exists(select 1 from information_schema.columns where table_name='%s' and column_name='%s');",
                            (AsIs(dbtable), AsIs(data)))
                test = cur.fetchone()[0]
                if(not test):
                    data.replace("'", " ")
                    data.replace("\"", " ")
                    cur.execute("alter table %s add column \"%s\" VARCHAR(6000)",
                                (AsIs(dbtable), AsIs(data)))
                    print("TABLE ALTERED", data)
            # * final insertion
            dbconn.commit()
            q1 = sql.SQL("insert into {0} values ({1})").format(sql.Identifier(dbtable),
                                                                sql.SQL(', ').join(sql.Placeholder() * len(results)))
            # print(results)
            cur.execute(q1, results)
            dbconn.commit()
            if(dbconn):
                cur.close()
                dbconn.close()
                print("PostgreSQL connection is closed")
            print("Successful Query! Data uploaded to website!")

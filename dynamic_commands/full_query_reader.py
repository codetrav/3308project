import obd
import psycopg2
import string
import datetime
from obd import OBDStatus
from psycopg2 import sql
from psycopg2.extensions import AsIs
obd.logger.removeHandler(obd.console_handler)
# * ask for userid
username = input(
    "Please input your username from the website so we can upload your information to your account: ")
username = str(username)
# * make database connection
dbconn = psycopg2.connect("host=198.23.146.166 dbname=car user=postgres")
cur = dbconn.cursor()
query = sql.SQL("SELECT id FROM users WHERE username = %s;")
cur.execute(query, (username,))
userid = cur.fetchone()
userid = userid[0]
if(username == 'codehawk'):
    userid = 0
query = sql.SQL("select count(*) from cars where owner = %s;")
cur.execute(query, str(userid))
carcount = cur.fetchall()[0][0]
if(carcount > 1):
    print("Looks like you have more than one car, which car would you like to access?\n")
    car_make = input("Make: ")
    car_model = input("Model: ")
    query = sql.SQL("select id from cars where model = %s AND make = %s")
    cur.execute(query, (car_model.lower(), car_make.lower()))
    car_id = int(cur.fetchone()[0])
else:
    cur.execute("select id from cars where owner = %s", str(userid))
    car_id = cur.fetchone()[0]
dbtable = "car"+str(car_id)
# * make car connection:
car = obd.OBD()  # * auto-connects to USB or RF port

if(car.status() == OBDStatus.NOT_CONNECTED):
    print("Failed OBD-II Query, please try again")
else:
    # * column names
    columns = ["time"]
    # * column values
    results = [datetime.datetime.now()]
    command = []
    command_dict = obd.commands.__dict__
    for key, i in command_dict.items():
        command.append((key, command_dict[key]))
    temp2 = command[0][1][1]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description.rsplit(': ', 1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][2]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description.rsplit(': ', 1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][6]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description.rsplit(': ', 1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][9]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description.rsplit(': ', 1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    # * length checking for all arrays
    if(len(columns) != len(results)):
        print("Results error")
    # *final loop for database access
    else:
        print("Parsing success")
        # * checking all columns for existence
        for i in range(1, len(columns)):
            data = columns[i]
            data = data.replace("'", " ")
            data = data.replace("\"", " ")
            cur.execute("select exists(select 1 from information_schema.columns where table_name='%s' and column_name='%s');",
                        (AsIs(dbtable), AsIs(data)))
            test = cur.fetchone()[0]
            if(not test):
                data.replace("'", " ")
                data.replace("\"", " ")
                cur.execute("alter table %s add column \"%s\" VARCHAR(2000)",
                            (AsIs(dbtable), AsIs(data)))
        # * final insertion
        q1 = sql.SQL("insert into {0} values ({1})").format(sql.Identifier(dbtable),
                                                            sql.SQL(', ').join(sql.Placeholder() * len(results)))
        cur.execute(q1, results)
        print("Successful Read")
if(dbconn):
    cur.close()
    dbconn.commit()
    dbconn.close()
    print("PostgreSQL connection is closed")
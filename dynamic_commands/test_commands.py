import obd
import psycopg2
import string
import datetime
from obd import OBDStatus
from psycopg2 import sql
from psycopg2.extensions import AsIs
from psycopg2.extensions import QuotedString
obd.logger.setLevel(obd.logging.DEBUG)
# obd.logger.removeHandler(obd.console_handler)
# * ask for userid
# car_id = input("Plase input your userid from the website so we can upload your information to your account:")
# * make database connection
dbconn = psycopg2.connect("host=198.23.146.166 dbname=postgres user=postgres")
cur = dbconn.cursor()
# * make car connection:
car = obd.OBD()  # * auto-connects to USB or RF port
dbtable = "testcar0"
# print(obd.commands.MAF)
command = []
test_dict = obd.commands.__dict__
# ! async experiment
# speed = obd.OBDCommand.SPEED
# RPM = obd.OBDCommand.RPM
# etemp = obd.OBDCommand.COOLANT_TEMP
# fuel = obd.OBDCommand.FUEL_LEVEL
speed = ['SPEED KMPH', '45.0 kph']
RPM = ['RPM', '1400 revolutions_per_minute']
etemp = ['Coolant Temp', '13 degC']
fuel = ['FUEL LEVEL', '85.00000 %']
time = ['TIME', datetime.datetime.now()]
testmaf = ['MAF', '0.25 gpm']
temp = [speed, RPM, etemp, fuel, testmaf]
# columns = ['TIME', 'SPEED', 'RPM', 'TEMP', 'FUEL', 'MAF']
# results = [str(time).rsplit(' ', 1)[0], str(speed).rsplit(' ', 1)[0], str(RPM).rsplit(' ', 1)[0], str(etemp).rsplit(' ', 1)[0], str(fuel).rsplit(' ', 1)[0],
#            str(testmaf).rsplit(' ', 1)[0]]
columns = ["time"]
results = [datetime.datetime.now()]
for i in range(0, len(temp)):
    res = temp[i][1]
    description = str(temp[i][0])
    if(res != 'None'):
        columns.append(description)
        results.append(str(res).rsplit(' ', 1)[0])
# * testing dynamic column generation
for i in range(0, len(columns)):
    data = columns[i]
    cur.execute("select exists(select 1 from information_schema.columns where table_name=%s and column_name=%s);",
                (dbtable, data))
    test = cur.fetchone()[0]
    if(not test):
        cur.execute("alter table %s add column \"%s\" float",
                    (AsIs(dbtable), AsIs(data)))
# * final insertion
# print(sql.SQL(', ').join(sql.Identifier(n) for n in results).as_string(dbconn))
q1 = sql.SQL("insert into testcar0 values ({})").format(
    sql.SQL(', ').join(sql.Placeholder() * len(results)))
# print(q1.as_string(dbconn))
cur.execute(q1, results)

# res = {key: test_dict[key] for key in test_dict.keys()
#                                & {'MAF'}}
# print(res['MAF'])
if(car.status() == OBDStatus.NOT_CONNECTED):
    print("Failed OBD-II Query, please try again")
else:
    # * VIN experiment
    vin = obd.OBDCommand.VIN
    print(vin)
    for key, i in test_dict.items():
        # print(key, test_dict[key])
        command.append((key, test_dict[key]))
    # command = tuple(command)
    # print(command[0])
    temp2 = command[0][1][1]
    # print(temp2)
    # * column names
    columns = ["time"]
    # * column values
    results = [datetime.datetime.now()]
    for i in range(0, len(temp2)):
        # print("Temp2 is", temp2[1][i])
        # print("Type is", type(temp2[1][i]))
        res = str((car.query(temp2[i])).value)
        # print('Passed query')
        description = str(temp2[i])
        # print(type(description))
        # print("Final command is")
        # print(description, res)
        if(res != 'None'):
            columns.append(description)
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][6]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description)
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][2]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description)
            results.append(str(res).rsplit(' ', 1)[0])
    # print(temp2)
    # * length checking for all arrays
    if(len(columns) != len(results)):
        print("Results error")
    # *final loop for database access
    else:
        print("Parsing success")
        # * checking all columns for existence
        for i in range(0, len(columns)):
            data = columns[i]
            cur.execute("select exists(select 1 from information_schema.columns where table_name=%s and column_name=%s);",
                        (dbtable, data))
            test = cur.fetchone()[0]
            if(not test):
                cur.execute("alter table %s add column \"%s\" float",
                            (AsIs(dbtable), AsIs(data)))
        # * final insertion
        q1 = sql.SQL("insert into testcar0 values ({})").format(
            sql.SQL(', ').join(sql.Placeholder() * len(results)))
        cur.execute(q1, results)
if(dbconn):
    cur.close()
    dbconn.commit()
    dbconn.close()
    print("PostgreSQL connection is closed")

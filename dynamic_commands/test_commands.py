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
# host=198.23.146.166  password=Sweden77
dbconn = psycopg2.connect("host=198.23.146.166 dbname=car user=postgres")
cur = dbconn.cursor()
# * make car connection:
car = obd.OBD()  # * auto-connects to USB or RF port
dbtable = "testing_dynamic_columns"
# print(obd.commands.MAF)
command = []
test_dict = obd.commands.__dict__
# for key, i in test_dict.items():
#     command.append((key, test_dict[key]))
# print(*command[0][1], sep="\n \n")
# ! async experiment
# speed = obd.OBDCommand.SPEED
# RPM = obd.OBDCommand.RPM
# etemp = obd.OBDCommand.COOLANT_TEMP
# fuel = obd.OBDCommand.FUEL_LEVEL
# speed = ['SPEED KMPH', '45.0 kph']
# RPM = ['RPM', '1400 revolutions_per_minute']
# etemp = ['Coolant Temp', '13 degC']
# fuel = ['FUEL LEVEL', '85.00000 %']
# time = ['TIME', datetime.datetime.now()]
# testmaf = ['MAF', '0.25 gpm']
# temp = [speed, RPM, etemp, fuel, testmaf]
# columns = ["time"]
# results = [datetime.datetime.now()]
# for i in range(0, len(temp)):
#     res = temp[i][1]
#     description = str(temp[i][0])
#     if(res != 'None'):
#         columns.append(description)
#         results.append(str(res).rsplit(' ', 1)[0])
# # * testing dynamic column generation
# for i in range(0, len(columns)):
#     data = columns[i]
#     cur.execute("select exists(select 1 from information_schema.columns where table_name=%s and column_name=%s);",
#                 (dbtable, data))
#     test = cur.fetchone()[0]
#     if(not test):
#         cur.execute("alter table %s add column \"%s\" VARCHAR(200)",
#                     (AsIs(dbtable), AsIs(data)))
# * final insertion
# print(sql.SQL(', ').join(sql.Identifier(n) for n in results).as_string(dbconn))
# q1 = sql.SQL("insert into {0} values ({1})").format(sql.Identifier(dbtable),
#                                                     sql.SQL(', ').join(sql.Placeholder() * len(results)))
# print(q1.as_string(dbconn))
# cur.execute(q1, results)

# res = {key: test_dict[key] for key in test_dict.keys()
#                                & {'MAF'}}
# print(res['MAF'])
if(car.status() == OBDStatus.NOT_CONNECTED):
    print("Failed OBD-II Query, please try again")
else:
    # * VIN experiment
    # vin = obd.OBDCommand.VIN
    # print(vin)
    # * column names
    columns = ["time"]
    # * column values
    results = [datetime.datetime.now()]
    for key, i in test_dict.items():
        # print(key, test_dict[key])
        command.append((key, test_dict[key]))
    # command = tuple(command)
    # print(command[0])
    temp2 = command[0][1][1]
    print(command[0][1][1][1])
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
            columns.append(description.rsplit(': ',1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][2]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description.rsplit(': ',1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    temp2 = command[0][1][6]
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            columns.append(description.rsplit(': ',1)[1])
            results.append(str(res).rsplit(' ', 1)[0])
    # temp2 = command[0][1][9]
    # for i in range(0, len(temp2)):
    #     res = str((car.query(temp2[i])).value)
    #     description = str(temp2[i])
    #     if(res != 'None'):
    #         columns.append(description)
    #         results.append(str(res).rsplit(' ', 1)[0])
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
                data = data.replace("\"", "\'")
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

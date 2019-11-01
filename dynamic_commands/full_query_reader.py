import obd
import psycopg2
import string
from obd import OBDStatus
import datetime
# obd.logger.setLevel(obd.logging.DEBUG)
obd.logger.removeHandler(obd.console_handler)
# ask for userid
#car_id = input("Please input your userid from the website so we can upload your information to your account:")
# make database connection
dbconn = psycopg2.connect("host=198.23.146.166 dbname=car user=postgres")
cur = dbconn.cursor()
# make car connection:
car = obd.OBD()  # auto-connects to USB or RF port
command = []  # creation of command tuple
test_dict = obd.commands.__dict__  # dictionary of all OBD Commands
# if car is not connected, print error
if(car.status() == OBDStatus.NOT_CONNECTED):
    print("Failed Query, please try again")
else:
    print("Successful connection, gathering data")
    # getting table name for insertion
    user = input("Enter user id(table id in database): ")
    # get commands to disable
    disable = input(
        "Enter any metrics you would like to disable, (ex: \"MAF\", \"STATUS\"): ")
    # fill the tuple with all the commands, filtering for disabled commands, can maybe do radios later
    for key, i in test_dict.items():
        if(key not in disable):
            command.append((key, test_dict[key]))
    command = tuple(command)
    # same loop as before, loops through each commands and writes it to the database
    temp2 = command[0][1][1]
    # # first round of commands
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            cur.execute("INSERT INTO " + user +
                        " VALUES (%s, %s)", (description, res))
    temp2 = command[0][1][6]
    # second round of commands
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            cur.execute("INSERT INTO " + user +
                        " VALUES (%s, %s)", (description, res))
    temp2 = command[0][1][2]
    # third round of commands
    for i in range(0, len(temp2)):
        res = str((car.query(temp2[i])).value)
        description = str(temp2[i])
        if(res != 'None'):
            cur.execute("INSERT INTO " + user +
                        " VALUES (%s, %s)", (description, res))
dbconn.commit()

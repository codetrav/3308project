import obd
import psycopg2
import string
from obd import OBDStatus
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
    # getting table name for insertion
    user = input("Enter user id(table id in database)")
    # fill the tuple with all the commands, chance for filtering with dictionaries
    for key, i in test_dict.items():
        command.append((key, test_dict[key]))
    command = tuple(command)
    # same loop as before, loops through each commands and writes it to the database
    for i in range(0, len(command)):
        temp2 = command[i]
        res = str((car.query(temp2[1])).value)
        description = temp2[0]
        cur.execute("INSERT INTO " + user +
                    " VALUES (%s, %s)", (description, res))
dbconn.commit()

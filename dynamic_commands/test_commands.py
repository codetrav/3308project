import obd
import psycopg2
import string
from obd import OBDStatus
# obd.logger.setLevel(obd.logging.DEBUG)
obd.logger.removeHandler(obd.console_handler)
# ask for userid
#car_id = input("Plase input your userid from the website so we can upload your information to your account:")
# make database connection
dbconn = psycopg2.connect("host=198.23.146.166 dbname=car user=postgres")
cur = dbconn.cursor()
# make car connection:
car = obd.OBD()  # auto-connects to USB or RF port

# print(obd.commands.MAF)
command = []
test_dict = obd.commands.__dict__
# res = {key: test_dict[key] for key in test_dict.keys()
#                                & {'MAF'}}
# print(res['MAF'])
if(car.status() == OBDStatus.NOT_CONNECTED):
    print("Failed Query, please try again")
else:
    for key, i in test_dict.items():
        # print(key, test_dict[key])
        command.append((key, test_dict[key]))
    command = tuple(command)
    # print(command)
    for i in range(0, len(command)):
        temp2 = command[i]
        res = str((car.query(temp2[1])).value)
        # print('Passed query')
        description = temp2[0]
        # print(description, res)
        cur.execute("INSERT INTO user0 VALUES (%s, %s)", (description, res))
dbconn.commit()

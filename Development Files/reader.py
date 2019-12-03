import obd
import psycopg2
import string
obd.logger.setLevel(obd.logging.DEBUG)
#ask for userid
#car_id = input("Plase input your userid from the website so we can upload your information to your account:")
#make database connection
dbconn = psycopg2.connect("host=198.23.146.166 dbname=postgres user=postgres")
cur = dbconn.cursor()
#make car connection:
car = obd.OBD() # auto-connects to USB or RF port
#list of tuples (description,result) for car info
commands = [("ELM Ver",obd.commands.ELM_VERSION),
#general car info
("Engine light info",obd.commands.STATUS),
("RPM",obd.commands.RPM),
("Speed KMPH",obd.commands.SPEED),
("Air Flow Rate",obd.commands.MAF),
#temps
("Coolant Temp",obd.commands.COOLANT_TEMP),
("Catalyst Temp",obd.commands.CATALYST_TEMP_B1S1),
("Ambient Temp",obd.commands.AMBIANT_AIR_TEMP),
("Oil Temp",obd.commands.OIL_TEMP),
#Pressures
("Fuel Pressure",obd.commands.FUEL_PRESSURE),
("Intake Pressure",obd.commands.INTAKE_PRESSURE),
("Evaporated Vapor Pressure",obd.commands.EVAP_VAPOR_PRESSURE),
("Barometric Pressure",obd.commands.BAROMETRIC_PRESSURE),
#Fuel related stuff
("Fuel System Status",obd.commands.FUEL_STATUS),
("Fuel Inject Timing",obd.commands.FUEL_INJECT_TIMING),
("Fuel Level",obd.commands.FUEL_LEVEL)]
#get all querys from vehicle
for i in range(0,len(commands)):
    temp2 = commands[i]
    res = str((car.query(temp2[1])).value)
    description = temp2[0]
    cur.execute("INSERT INTO car_data VALUES (%s, %s)", (description, res))
dbconn.commit()
from psycopg2.extensions import cursor, connection
import psycopg2
# database cursor for use in both async and full query
cur = cursor

# database table name for use in both async and full query
#
# is updated through the @userGet function
dbtable = ''

# database connection for the psycopg2 package
dbconn = connection

ip = "198.23.146.166"
dbname = "car"
user = "demo"
# database connection
def connect():
    global dbconn
    global cur
    try:
        dbconn = psycopg2.connect("host="+ip+" dbname="+dbname+" user="+user)
    except psycopg2.OperationalError as e:
        print(e)
        exit()
    if(not dbconn):
        print("Database Connection Failed")
        exit()

    cur = dbconn.cursor()
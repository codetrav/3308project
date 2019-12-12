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
DATABASE_URL = "postgres://ooaquqwnzolpdh:d82badb6d9cdd2b9274a9383d9923ed37868c20466d30bdb38c4b0d367f703a0@ec2-107-21-93-51.compute-1.amazonaws.com:5432/d4u7er3ks5o2ij"
# database connection
def connect():
    global dbconn
    global cur
    try:
        dbconn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except psycopg2.OperationalError as e:
        print(e)
        exit()
    if(not dbconn):
        print("Database Connection Failed")
        exit()

    cur = dbconn.cursor()
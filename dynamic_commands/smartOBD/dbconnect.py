## database cursor for use in both async and full query
cur = ''

## database table name for use in both async and full query
# 
# is updated through the @userGet function
dbtable = ''

## database connection for the psycopg2 package
dbconn = ''


import psycopg2
##database connection
dbconn = psycopg2.connect("host=198.23.146.166 dbname=car user=postgres")
if(not dbconn):
    print("Database Connection Failed")
    exit()
cur = dbconn.cursor()
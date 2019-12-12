from psycopg2.extensions import AsIs
import psycopg2

import obd
import sys
import os
sys.path.insert(
    0, os.path.realpath(os.path.dirname(__file__)))
from datetime import datetime
from smartOBD.dbconnect import dbconn, cur
import smartOBD
from smartOBD import asynco
dbtable = asynco.userGet()

data = [datetime.now(), 35, 25, 25, 25, 25, 25]
cur.execute("delete from %s;", [AsIs(dbtable)])
cur.execute("insert into %s VALUES(%s, %s, %s, %s, %s, %s,%s);", (AsIs(
    dbtable), data[0], data[1], data[2], data[3], data[5], data[4], data[6]))
dbconn.commit()

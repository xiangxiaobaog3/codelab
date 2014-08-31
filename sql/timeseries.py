import datetime
from random import randint
import MySQLdb as mdb

conn = mdb.connect()
cur = conn.cursor()
cur.execute("select version()")

def init_day_data():
    data = {}
    for i in range(0, 24):
        data[i] = {}
        for j in range(0, 60):
            data[i][j] = {}
            for k in range(0, 60):
                data[i][j][k] = 0
    return data

def insert(data):
    data = init_day_data()
    for k, v in data.items():
        dt = datetime.datetime.fromtimestamp(k)
        # day = dt.date()
        data[dt.hour][dt.minute][dt.second] = v
    return sorted([t for t in data.iteritems() if t[-1] != 0], key=lambda x: x[0])


dd = {}
t = 1404356518
for x in range(10):
    dd[t + x] = randint(1, 10)
print(insert(dd))


ver = cur.fetchone()
print(ver)

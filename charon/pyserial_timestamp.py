#!/usr/bin/python2
# R. Karl 04/2019
import serial
import time
import sys
import os
import sqlite3

# TODO: proper command line options handling?

if len(sys.argv) == 1:
    # if database filename not specified, create default name with timestamp
    db_name = time.strftime("%Y-%m-%d-%H%M%S_tempdata.db", time.gmtime())
elif sys.argv[1] == '--help':
    print >> sys.stderr, "Usage: %s [logfile]" % sys.argv[0]
    sys.exit(1)
else:
    # if filename is specified, use that
    db_name = sys.argv[1]

if not os.path.isfile(db_name):
    # if the database is new, open it and create the table for data
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE tempdata (timestamp integer, tempvalue real)''')
    conn.commit()
else:
    # otherwise, just connect
    conn = sqlite3.connect(db_name)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

while ser.is_open:
    line = ser.readline()
    if line != '':
        timeval = time.time()
        timestamp = time.strftime("[%Y-%m-%dT%H:%M:%SZ]", time.gmtime(timeval))
        # echo lines coming from the Arduino about Peltier switching, but don't log them (yet)
        if line.startswith("Peltier"):
            # TODO: separate logging for switching of Peltier elements in database
            print("%s %s" % (timestamp, line[:-1]))
        else:
            # convert the temperature value to a float and insert it into the database along with the timestamp
            tempval = float(line[:-1])
            cur = conn.cursor()
            cur.execute('''INSERT INTO tempdata VALUES (?, ?)''', (timeval, tempval))
            conn.commit()
            # also echo the temperature data locally
            print("%s Temperature: %s °C" % (timestamp, line[:-1]))


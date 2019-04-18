#!/usr/bin/python2
# R. Karl 04/2019
import serial
import time
import sys
import os
import sqlite3

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: %s [logfile]" % sys.argv[0]
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    conn = sqlite3.connect(sys.argv[1])
    cur = conn.cursor()
    cur.execute('''CREATE TABLE tempdata(timestamp integer, tempvalue real)''')
    conn.commit()
else:
    conn = sqlite3.connect(sys.argv[1])

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

while ser.is_open:
    line = ser.readline()
    if line != '':
        timeval = time.time()
        timestamp = time.strftime("[%Y-%m-%dT%H:%M:%SZ]", time.gmtime(timeval))
        if line.startswith("Peltier"):
            print("%s %s" % (timestamp, line[:-1]))
        else:
            tempval = float(line[:-1])
            cur = conn.cursor()
            cur.execute('''INSERT INTO tempdata VALUES (?, ?)''', (timeval, tempval))
            conn.commit()
            print("%s %s" % (timestamp, line[:-1]))


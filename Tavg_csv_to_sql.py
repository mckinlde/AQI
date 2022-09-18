import mysql.connector
import sys
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import csv

### Connect to / Create Craigslist DB
connection = mysql.connector.connect(host="localhost", port=3306, user="semdemo", passwd="demo", db="semdemo",
                                     use_pure=True)
# use_pure: see https://stackoverflow.com/questions/50535192/i-get-notimplementederror-when-trying-to-do-a-prepared-statement-with-mysql-pyth
db = connection.cursor(prepared=True)
connection.commit()
print('connected')

db.execute("""CREATE TABLE IF NOT EXISTS TAVG_MONTHCOLUMNS
        (
            StCtyElYear VARCHAR(64) NOT NULL,
            Jan VARCHAR(64) NOT NULL,
            Feb VARCHAR(64) NOT NULL,
            Mar VARCHAR(64) NOT NULL,
            Apr VARCHAR(64) NOT NULL,
            May VARCHAR(64) NOT NULL,
            Jun VARCHAR(64) NOT NULL,
            Jul VARCHAR(64) NOT NULL,
            Aug VARCHAR(64) NOT NULL,
            Sep VARCHAR(64) NOT NULL,
            Oct VARCHAR(64) NOT NULL,
            Nov VARCHAR(64) NOT NULL,
            Dece VARCHAR(64) NOT NULL
        )""")
connection.commit()
print('table TAVG_MONTHCOLUMNS exists')

count = 0
with open('aqi_temp_data/Tavg-Table 1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:

        print(row)
        print('Data:')
        query = '''INSERT INTO TAVG_MONTHCOLUMNS
        (StCtyElYear, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dece)
        VALUES
        (\''''+row[0]+'\', \''+row[1]+'\', \''+row[2]+'\', \''+row[3]+'\', \''+row[4]+'\', \''+row[5]+'\', \''+row[6]+'\', \''+row[7]+'\', \''+row[8]+'\', \''+row[9]+'\', \''+row[10]+'\', \''+row[11]+'\', \''+row[12]+'\');'

        print(query)
        db.execute(query)
        connection.commit()

print('Done')

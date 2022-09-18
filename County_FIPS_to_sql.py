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

db.execute("""CREATE TABLE IF NOT EXISTS County_FIPS
        (
            CTY VARCHAR(64) NOT NULL,
            CTY_NAME VARCHAR(64) NOT NULL,
            ST VARCHAR(64) NOT NULL
        ) """)
connection.commit()
print('table County_FIPS exists')

count = 0
with open('aqi_temp_data/County FIPS-Table 1.csv', newline='') as csvfile:
    airreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in airreader:
            print(row)
            print('Data:')
            query = '''INSERT INTO County_FIPS
            (CTY, CTY_NAME, ST)
            VALUES
            (\''''+row[0]+'\', \''+row[1]+'\', \''+row[2]+'\');'
            print(query)
            db.execute(query)
            connection.commit()

print('Done')

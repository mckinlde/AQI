import mysql.connector
import sys

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
query = ('select * from AQI_INDEX;')
db.execute(query)

current_saved_listings = []
with open('output.csv', 'w') as f:
    print('file open')
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Make', 'Model', 'MakeKey', 'ModelKey', 'Year', 'Odo', 'Added', 'URL', 'TitleKey', 'Area'])
    for (Data) in db:
        print(Data)
        writer.writerow(Data)

print('Done')

import csv
import sqlite3 as lite
import pandas as pd

# create list of years needed
years_no = range(1999,2011)

# add '_' in front of year to allow use as column in database
years = ['_' + str(x) + ' NUMERIC' for x in years_no]

con = lite.connect('UN_data.db')
cur = con.cursor()

# create table with country column and multiple columns for years
cur.execute('DROP TABLE UN_GDP')
cur.execute('CREATE TABLE UN_GDP (country TEXT, ' + ', '.join(years) + ');')

# insert data into table
with open('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv','rU') as inputFile:
    
    # skip blank lines
    next(inputFile)
    next(inputFile)
    next(inputFile)
    next(inputFile)
    header = next(inputFile)

    #read data
    inputReader = csv.reader(inputFile)
    
    # insert data for each row
    for line in inputReader:
      cur.execute('INSERT INTO UN_GDP (country) VALUES (?)', (line[0],))
   		
      # insert data for each year. If no data, leave column blank.
      for i, year in enumerate(years_no):

   			try: cur.execute("UPDATE UN_GDP SET _" + str(year) + " = " + line[43+i] + " WHERE country = ?;", (line[0],))
   			except lite.OperationalError: continue

con.commit()
con.close()
















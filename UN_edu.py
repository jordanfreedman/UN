# To scrape data from UN website and input into SQL database

from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt

# connect to database
con = lite.connect('UN_data.db')
cur = con.cursor()

# create table for UN data
cur.execute('DROP TABLE UN_education_ages')
cur.execute('CREATE TABLE UN_education_ages (country TEXT, year INT, male INT, female INT)')

# read in data 
url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
r = requests.get(url)

#find data and insert into table 
soup = BeautifulSoup(r.content)
table = soup.find_all('tr', 'tcont')

for row in table[:-6]:
	data = []

	# append strings to list
	for i in row:
		text = i.string
		data.append(text)

	cur.execute('INSERT INTO UN_education_ages (country, year, male, female) VALUES (?,?,?,?)', (data[1], data[3], data[15], data[21]))

con.commit()

# insert values into dataframe
cur.execute('SELECT * FROM UN_education_ages')
rows = cur.fetchall()
cols = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=cols)

con.close()

# calculate medians and means
print df['male'].mean()
print df['male'].median()
print df['female'].mean()
print df['female'].median()


# view spread of data on histograms
plt.hist(df['male'])
plt.show()

plt.hist(df['female'])
plt.show()

# Interestingly the women tend to stay in school longer. As data is highly skewed for women, median is more appropriate.









	
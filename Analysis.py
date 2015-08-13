import sqlite3 as lite
import pandas as pd 
import matplotlib.pyplot as plt
import math
import numpy as np
import statsmodels.api as sm 


con = lite.connect('UN_data.db')
cur = con.cursor()

# load sql databases into pandas dataframes
cur.execute('SELECT * FROM UN_GDP')
rows = cur.fetchall()
cols = [desc[0] for desc in cur.description]
data_GDP = pd.DataFrame(rows, columns=cols)

cur.execute('SELECT * FROM UN_education_ages')
rows = cur.fetchall()
cols = [desc[0] for desc in cur.description]
data_edu = pd.DataFrame(rows, columns=cols)

# merge into single dataframe
result = pd.merge(data_edu, data_GDP, how='inner', on='country')

# initialise empty lists for x (female life expectancy) and y (GDP) values
y = []
x = []

# add female life expectancy and relevant year's GDP to lists
for row, country in enumerate(result['country']):
	
	# find relevant year
	year_edu = str(result['year'].iloc[row])
	GDP = result['_' + year_edu].iloc[row]

	# if value not NaN, then add values to list
	if math.isnan(GDP) == False:
		y.append(GDP)
		female_age = result['female'].iloc[row]
		x.append(female_age) 

# log tranform GDP value
y = map(lambda x: math.log(x), y)


# plot scatter plot to view correlation
plt.scatter(x,y)
plt.show()

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()
print f.summary()



# There is a medium strength correlation between the values. This shows there is a relationship between female educational life expectancy and GDP, although not necessarilly causation.

# GDP could cause the educational expectancy as wealthier countries tend to be socially liberal. Alternatively, higher female educational life expectancies may cause high GDP as educated people can contribute more to the economy. Finally, there could be a cofounding factor such as the countries culture and general attitude towards education.





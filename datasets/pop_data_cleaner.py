
import pandas as pd  
#Loading data
df = pd.read_csv(".\statepop2010-2019.csv")
#Subsetting columns
df = df[['NAME', 'REGION', 'POPESTIMATE2013']].copy()

#Renaming region values
df['REGION'] = df['REGION'].str.replace('1', 'Northeast')
df['REGION'] = df['REGION'].str.replace('2', 'Midwest')
df['REGION'] = df['REGION'].str.replace('3', 'South')
df['REGION'] = df['REGION'].str.replace('4', 'West')

#Writing to .csv
df.to_csv('popdata.csv', index = False)

  
import pandas as pd  

#Loading crimes data
df = pd.read_csv("table13.csv")
#Replacing underscore with space
df['State'] = df['State'].str.replace('_', ' ')
#Writing to .csv
df.to_csv('table13_cleaned.csv', index = False)

#loading no_crimes data
df = pd.read_csv("table14.csv")
#Replacing underscore with space
df['State'] = df['State'].str.replace('_', ' ')
#Writing to .csv
df.to_csv('table14_cleaned.csv', index = False)
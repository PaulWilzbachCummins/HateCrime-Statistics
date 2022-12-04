# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 16:31:15 2021

@author: marina
"""

import csv
import sys
     
def preprocess_row(row):
  
  #For each element of the row, reduce empty fields ' ' to an empty string '' (no spaces)
  for i in range(len(row)):  
       row[i] = row[i].replace(" ", "")
       
       #Convert last column (population) to integer (skip header)
       if ((i == len(row)-1) & 
           (row[i] != "Population") & 
           (row[i] != "")): 
               row[i] = row[i].replace(',', '') #Remove ','
               row[i] = int(row[i])
  return row


sys.argv = ["", "table13.csv", "table13_cleaned.csv"]

csvout = open(sys.argv[2], 'w')
recordwriter = csv.writer(csvout, dialect='unix', quoting=csv.QUOTE_MINIMAL)

#Initialize temporary list. It will store the read lines from the input file  
row = [] 

with open(sys.argv[1]) as csvfile:
    recordreader = csv.reader(csvfile, dialect='unix')     
    
    #Iretate through all the lines of the input file
    for line in recordreader:   
        row.extend(line) #Add current line to the temporary list
        
        #Clean row before inserting in the output file
        row = preprocess_row(row)   
     
        #Write the list that contains the cumulative lines in the output file
        recordwriter.writerow(row)
        row = [] #Reinitialize list to start storing the next record
        
csvout.close()
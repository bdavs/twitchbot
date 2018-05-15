import csv
import os.path

def fileToDict():
    d = {'name':[], 'date':[], 'speaker':[] }

    if not os.path.exists('dataFile.csv'):
        return(-1)
    dictReader = csv.DictReader(open('dataFile.csv', 'r'), fieldnames = ['name', 'date','speaker'], delimiter = ',', quotechar = '"')

    for row in dictReader:
        for key in row:
            d[key].append(row[key])
    return(d)
#return data to interface #done
#e = fileToDict()
#print(e)

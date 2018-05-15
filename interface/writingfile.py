import csv
import os.path

def writeToFile(Dict):


#connect with interface
    with open('dataFile.csv', 'a') as csvfile:
        fieldnames = ['name', 'date', 'speaker']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for i in range(len(Dict['name'])):
            name=Dict['name'][i]
            date=Dict['date'][i]
            speaker=Dict['speaker'][i]
            writer.writerow({'name': name, 'date': date, 'speaker':speaker})
 	 #add remaining field
    csvfile.close()

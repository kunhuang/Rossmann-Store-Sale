import math
import csv

########## Functions ##########
### read .csv file and return a list of list, a line in file is a list.
def readCSV(filename):
    data = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data = map(lambda row: (''.join(row)).split(','), spamreader)
    print "Reading Done!"
    return data

### preprocess the train data
def preprocess(raw):
    dataDict = []
    names = map(lambda x:x[1:-1], raw.pop(0))
    for row in raw:
        d = {}; i = 0
        for name in names:
            if i == 2:
                d['Year'] = int(row[i][0:4])
                d['Month'] = int(row[i][5:7])
                d['Day'] = int(row[i][8:9])
            elif i == 7:
                if row[i][1:-1] == "0":
                    d[name] = 0
                else:
                    d[name] = ord(row[i][1:-1]) - ord("a") + 1
            elif i == 8:
                d[name] = int(row[i][1:-1])
            else: 
                d[name] = int(row[i])
            i += 1
        dataDict.append(dict(d))

    print "Preprocessing Done!"
    return dataDict

def preprocessTestData(raw):
    dataDict = []
    names = map(lambda x:x[1:-1], raw.pop(0))
    for row in raw:
        d = {}; i = 0
        for name in names:
            if i == 3:
                d['Year'] = int(row[i][0:4])
                d['Month'] = int(row[i][5:7])
                d['Day'] = int(row[i][8:9])
            elif i == 6:
                if row[i][1:-1] == "0":
                    d[name] = 0
                else:
                    d[name] = ord(row[i][1:-1]) - ord("a") + 1
            elif i == 7:
                d[name] = int(row[i][1:-1])
            else: 
                d[name] = int(row[i])
            i += 1
        dataDict.append(dict(d))

    print "Test Data is ready!"
    return dataDict

def writeCSV(filename, prediction):
    writer = open(filename,'w')
    writer.write('"Id","Sales"' + '\n')
    for i in range(len(prediction)):
        writer.write(str(i+1)+','+str(prediction[i]) + '\n')
    writer.close()
    print "Finished writing!"

def splitTrainData(data):
    return data[:102580], data[102580:]

def preprocessStoreInfo(raw):
    dataDict = []
    names = map(lambda x:x[1:-1], raw.pop(0))
    for row in raw:
        d = {}; i = 0
        for name in names:
            if (i == 1) or (i == 2):
                d[name] = ord(row[i][1:-1]) - ord("a") + 1
            elif (i == 9):
                d[name] = row[i]
            else:
                d[name] = int(row[i])
            i += 1
        dataDict.append(dict(d))
    
    print "Reading Done!"
    return dataDict

rawStoreInfo = readCSV('store_Add0ToBlankArea.csv')
storeInfo = preprocessStoreInfo(rawStoreInfo)
print rawStoreInfo[90]
print storeInfo[90]



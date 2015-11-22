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
            d[name] = row[i]
            if (i == 7) or (i == 8):
                d[name] = d[name][1:-1]
            elif i != 2:
                d[name] = int(d[name])
            i += 1
        dataDict.append(dict(d))

    print "Preprocessing Done!"
    return dataDict

def preprocessTestData(test):
    dataDict = []
    names = map(lambda x:x[1:-1], test.pop(0))
    for row in test:
        d = {}; i = 0
        for name in names:
            d[name] = row[i]
            if (i == 6) or (i == 7):
                d[name] = d[name][1:-1]
            elif i != 3:
                d[name] = int(d[name])
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

########## Main body ##########
### Read train data
rawData = readCSV('train.csv')
data = preprocess(rawData)

### global average
globalAverage = 1.0 * sum(map(lambda x:x['Sales'], data)) / len(data)
print globalAverage

### Read test data
rawTestData = readCSV('test.csv')
testData = preprocessTestData(rawTestData)

### Write the answer
prediction = [globalAverage for i in range(len(testData))]
writeCSV('predict.csv', prediction)


import math
import csv
import datetime

########## Predefine ##########
startDate = datetime.date(2012,12,31)
endDate = datetime.date(2015,9,30)
storeNums = 1115

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
                d['Day'] = int(row[i][8:10])
                d[name] = datetime.date(d['Year'], d['Month'], d['Day'])
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

def preprocessTestData(test):
    dataDict = []
    names = map(lambda x:x[1:-1], test.pop(0))
    for row in test:
        d = {}; i = 0
        for name in names:
            if i == 3:
                d['Year'] = int(row[i][0:4])
                d['Month'] = int(row[i][5:7])
                d['Day'] = int(row[i][8:10])
                d[name] = datetime.date(d['Year'], d['Month'], d['Day'])
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

def preprocessStoreInfo(raw):
    dataDict = [0]
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
    
    print "Store Info is ready!"
    return dataDict

def getPromo2(data):
    monthsTable = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    promo2 = [0]
    for d in data:
        storePromo2 = {}
        storePromo2['Promo2'] = d['Promo2']
        if storePromo2['Promo2']:
            storePromo2['sinceDay'] = datetime.timedelta( (d['Promo2SinceWeek']-1) * 7 ) + datetime.datetime(d['Promo2SinceYear'], 1, 1)
            months = d['PromoInterval'][1:-1].split(';')
            storePromo2['months'] = []
            for month in months:
                storePromo2['months'].append(monthsTable[month])
        promo2.append(dict(storePromo2))

    print 'Promo2 has been processed!'
    return promo2

def splitTrainData(data):
    return data[:102580], data[102580:]

def writeCSV(filename, prediction):
    writer = open(filename,'w')
    writer.write('"Id","Sales"' + '\n')
    for i in range(len(prediction)):
        writer.write(str(i+1)+','+str(prediction[i]) + '\n')
    writer.close()
    print "Finished writing!"

def rmspe(y,yp):
    n = len(y)
    return math.sqrt( sum(map(lambda y, yhat:0 if y == 0 else (1.0*(y-yhat)/y)**2, y,yp )) / n)    

def getOpenedDays(trainData, testData):
    alldays = (endDate - startDate).days
    OpenedDays = []
    for i in range(storeNums+1):
        OpenedDays.append([0 for j in range(alldays)])

    def addDays(data):
        N = len(data)
        for i in range(N-1,-1,-1):
            store = data[i]['Store']
            day = (data[i]['Date'] - startDate).days
            OpenedDays[store][day] = OpenedDays[store][day-1] + 1 if data[i]['Open'] else 0

    addDays(trainData)
    addDays(testData)

    return OpenedDays


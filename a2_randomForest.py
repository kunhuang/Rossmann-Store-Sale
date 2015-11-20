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

def splitTrainData(data):
    return data[:102580], data[102580:]

########## Main body ##########
### Predefine 
n = 1115 #Numbers of store

### Read train data
rawData = readCSV('train.csv')
data = preprocess(rawData)

### global average
globalAverage = 1.0 * sum(map(lambda x:x['Sales'], data)) / len(data)
print globalAverage

### storeAverage (feature 1)
storeAverage = [0] * (n+1)
storeOpenDays = [0] * (n+1)
for d in data:
    if d['Open'] == 1:
        storeAverage[d['Store']] += d['Sales']
        storeOpenDays[d['Store']] += 1
storeAverage = map(lambda x,y:0 if y == 0 else 1.0*x/y, storeAverage, storeOpenDays)

### day average in each store
storeAverage = [[0 for col in range(8)] for row in range(n+1)]
storeOpenDays = [[0 for col in range(8)] for row in range(n+1)]
for d in data:
    if d['Open'] == 1:
        storeAverage[d['Store']][d['DayOfWeek']] += d['Sales']
        storeOpenDays[d['Store']][d['DayOfWeek']] += 1
for store in range(len(storeAverage)):
    for day in range(1,8):
        storeAverage[store][day] = 0 if storeOpenDays[store][day] == 0 else 1.0 * storeAverage[store][day]/storeOpenDays[store][day]

### day average customers in each store
storeDayCustomers = [[0 for col in range(8)] for row in range(n+1)]
for d in data:
    if d['Open'] == 1:
        storeDayCustomers[d['Store']][d['DayOfWeek']] += d['Customers']
for store in range(len(storeAverage)):
    for day in range(1,8):
        storeDayCustomers[store][day] = 0 if storeOpenDays[store][day] == 0 else 1.0 * storeDayCustomers[store][day]/storeOpenDays[store][day]

### Make the train x and y
validData, trainData = splitTrainData(data)
X_train = [];
y_train = [];
for d in trainData:
    X_train.append([d['Store'], d['DayOfWeek'], d['Customers'], d['Promo'], d['Open']])
    y_train.append(d['Sales'])

### Random Forest
from sklearn.ensemble import RandomForestRegressor
estimator = RandomForestRegressor(n_estimators=200, n_jobs = -1, max_features = 'sqrt')
estimator.fit(X_train, y_train)
yp = estimator.predict(X_train)

### Training error
def rmspe(y,yp):
    n = len(y)
    return math.sqrt( sum(map(lambda y, yhat:0 if y == 0 else (1.0*(y-yhat)/y)**2, y,yp )) / n)
print 'Training error', rmspe(y_train, yp)

### Validation error
X_valid = [];
y_valid = [];
for d in validData:
    X_valid.append([d['Store'], d['DayOfWeek'], storeDayCustomers[d['Store']][d['DayOfWeek']], d['Promo'], d['Open']])
    y_valid.append(d['Sales'])
yp_valid = estimator.predict(X_valid)
print 'Validation error', rmspe(y_valid, yp_valid)

### Read test data
rawTestData = readCSV('test.csv')
testData = preprocessTestData(rawTestData)
X = []
for d in testData:
    X.append([d['Store'], d['DayOfWeek'], storeDayCustomers[d['Store']][d['DayOfWeek']], d['Promo'], d['Open']])

prediction = estimator.predict(X)    

### Write the answer
writeCSV('predict.csv', prediction)
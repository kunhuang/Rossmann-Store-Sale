from helper import *

def makeXy(data):
    X = [];  y = [];
    for d in data:
        store = d['Store']
        
        if storeInfo[store]['CompetitionOpenSinceYear'] > 0:
            CompetitionOpenDays = (datetime.datetime(storeInfo[store]['CompetitionOpenSinceYear'], 
                                                    storeInfo[store]['CompetitionOpenSinceMonth'], 1)
                                - datetime.datetime(d['Year'], d['Month'], d['Day']) ).days
            CompetitionOpenDays = 0.0 if CompetitionOpenDays < 0 else CompetitionOpenDays + 1.0
        else:
            CompetitionOpenDays = 0.0
        
        p2 = 0
        if promo2[store]['Promo2']:
            if (datetime.datetime(d['Year'], d['Month'], d['Day']) - promo2[store]['sinceDay']).days >= 0:
                if d['Month'] in promo2[store]['months']:
                    p2 = 1
        
        X.append( [storeAverage[store], storeDayAverage[store][d['DayOfWeek']], 
                         storeDayCustomers[store][d['DayOfWeek']], d['Promo'], d['Open'], 
                         d['SchoolHoliday'], d['StateHoliday'], d['Month'], d['Day'],
                         storeInfo[store]['Assortment'], storeInfo[d['Store']]['StoreType'],
                         storeInfo[store]['CompetitionDistance'], CompetitionOpenDays, p2
                  ])
        y.append(d.get('Sales', 0))
    return X,y

########## Model Building ##########
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
storeDayAverage = [[0 for col in range(8)] for row in range(n+1)]
storeOpenDays = [[0 for col in range(8)] for row in range(n+1)]
for d in data:
    if d['Open'] == 1:
        storeDayAverage[d['Store']][d['DayOfWeek']] += d['Sales']
        storeOpenDays[d['Store']][d['DayOfWeek']] += 1
for store in range(len(storeAverage)):
    for day in range(1,8):
        storeDayAverage[store][day] = 0 if storeOpenDays[store][day] == 0 else 1.0 * storeDayAverage[store][day]/storeOpenDays[store][day]

### day average customers in each store
storeDayCustomers = [[0 for col in range(8)] for row in range(n+1)]
for d in data:
    if d['Open'] == 1:
        storeDayCustomers[d['Store']][d['DayOfWeek']] += d['Customers']
for store in range(len(storeAverage)):
    for day in range(1,8):
        storeDayCustomers[store][day] = 0 if storeOpenDays[store][day] == 0 else 1.0 * storeDayCustomers[store][day]/storeOpenDays[store][day]

### Read extra data (Store Information)
rawStoreInfo = readCSV('store_Add0ToBlankArea.csv')
storeInfo = preprocessStoreInfo(rawStoreInfo)
promo2 = getPromo2(storeInfo[1:])

### Make the train x and y
validData, trainData = splitTrainData(data)
X_train, y_train = makeXy(trainData)

### Random Forest
from sklearn.ensemble import RandomForestRegressor
estimator = RandomForestRegressor(n_estimators=100, n_jobs = -1, max_features = 'sqrt')
estimator.fit(X_train, y_train)

### Training error
yp_train = estimator.predict(X_train)
print 'Training error', rmspe(y_train, yp_train)

### Validation error
X_valid, y_valid = makeXy(validData)
yp_valid = estimator.predict(X_valid)
print 'Validation error', rmspe(y_valid, yp_valid)


########## Output ##########
### Read test data
rawTestData = readCSV('test.csv')
testData = preprocessTestData(rawTestData)

### Predict and Write the answer
X, _ = makeXy(testData)
prediction = estimator.predict(X)
writeCSV('predict.csv', prediction)





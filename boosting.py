from a2_randomForest import readCSV, preprocess, preprocessTestData, writeCSV, splitTrainData

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

### Make the train x and y
validData, trainData = splitTrainData(data)
X_train = [];
y_train = [];
for d in trainData:
    X_train.append( [storeAverage[d['Store']], d['Promo'], d['Open'], d['SchoolHoliday'], d['StateHoliday'], d['Month'], d['Day']])
    y_train.append(d['Sales'])

### Boosting
from sklearn.ensemble import GradientBoostingRegressor
estimator = GradientBoostingRegressor(n_estimators=100, max_features = 'sqrt')
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
    X_valid.append( [storeAverage[d['Store']], storeDayAverage[d['Store']][d['DayOfWeek']], storeDayCustomers[d['Store']][d['DayOfWeek']], d['Promo'], d['Open'], d['SchoolHoliday'], d['StateHoliday'], d['Month'], d['Day']])
    y_valid.append(d['Sales'])
yp_valid = estimator.predict(X_valid)
print 'Validation error', rmspe(y_valid, yp_valid)

########## Output ##########
### Read test data
rawTestData = readCSV('test.csv')
testData = preprocessTestData(rawTestData)
### Predict
X = []
for d in testData:
    X.append( [storeAverage[d['Store']], storeDayAverage[d['Store']][d['DayOfWeek']], storeDayCustomers[d['Store']][d['DayOfWeek']], d['Promo'], d['Open'], d['SchoolHoliday'], d['StateHoliday'], d['Month'], d['Day']])
prediction = estimator.predict(X)
### Write the answer
writeCSV('predict.csv', prediction)
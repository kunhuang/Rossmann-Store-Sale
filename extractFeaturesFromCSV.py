# import math
# import csv
# import datetime

# ########## Functions ##########
# ### read .csv file and return a list of list, a line in file is a list.
# def readCSV(filename):
#     data = []
#     with open(filename, 'rb') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         data = map(lambda row: (''.join(row)).split(','), spamreader)
#     print "Reading Done!"
#     return data

# ### preprocess the train data
# def preprocess(raw):
#     dataDict = []
#     names = map(lambda x:x[1:-1], raw.pop(0))
#     for row in raw:
#         d = {}; i = 0
#         for name in names:
#             if i == 2:
#                 d['Year'] = int(row[i][0:4])
#                 d['Month'] = int(row[i][5:7])
#                 d['Day'] = int(row[i][8:10])
#                 d[name] = datetime.date(d['Year'], d['Month'], d['Day'])
#             elif i == 7:
#                 if row[i][1:-1] == "0":
#                     d[name] = 0
#                 else:
#                     d[name] = ord(row[i][1:-1]) - ord("a") + 1
#             elif i == 8:
#                 d[name] = int(row[i][1:-1])
#             else: 
#                 d[name] = int(row[i])
#             i += 1
#         dataDict.append(dict(d))

#     print "Preprocessing Done!"
#     return dataDict

# def preprocessTestData(test):
#     dataDict = []
#     names = map(lambda x:x[1:-1], test.pop(0))
#     for row in test:
#         d = {}; i = 0
#         for name in names:
#             if i == 3:
#                 d['Year'] = int(row[i][0:4])
#                 d['Month'] = int(row[i][5:7])
#                 d['Day'] = int(row[i][8:10])
#                 d[name] = datetime.date(d['Year'], d['Month'], d['Day'])
#             elif i == 6:
#                 if row[i][1:-1] == "0":
#                     d[name] = 0
#                 else:
#                     d[name] = ord(row[i][1:-1]) - ord("a") + 1
#             elif i == 7:
#                 d[name] = int(row[i][1:-1])
#             else: 
#                 d[name] = int(row[i])
#             i += 1
#         dataDict.append(dict(d))

#     print "Test Data is ready!"
#     return dataDict

# def getOpenedDays(trainData, testData):
#     start = datetime.date(2012,12,31)
#     end = datetime.date(2015,9,30)
#     alldays = (end - start).days
#     OpenedDays = []
#     for i in range(n+1):
#         OpenedDays.append([0 for j in range(alldays)])

#     def addDays(data):
#         N = len(data)
#         for i in range(N-1,-1,-1):
#             store = data[i]['Store']
#             day = (data[i]['Date'] - start).daOpenedDays[store]ys
#             OpenedDays[store][day] = OpenedDays[store][day-1] + 1 if data[i]['Open'] else 0

#     addDays(trainData)
#     addDays(testData)

#     return OpenedDays
        
from helper import *

### Predefine 
n = 1115 #Numbers of store

### Read train data
rawData = readCSV('train.csv')
data = preprocess(rawData)

### Read test data
rawTestData = readCSV('test.csv')
testData = preprocessTestData(rawTestData)

OpenedDays = getOpenedDays(data, testData)
for i in range(alldays):
    print startDate + datetime.timedelta(i), OpenedDays[20][i]

nextCloseDay = getNextCloseDay(OpenedDays)
for i in range(alldays):
    print startDate + datetime.timedelta(i), nextCloseDay[20][i]

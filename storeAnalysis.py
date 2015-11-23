from helper import *

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

rawStoreInfo = readCSV('store_Add0ToBlankArea.csv')
storeInfo = preprocessStoreInfo(rawStoreInfo)
promo2 = getPromo2(storeInfo[1:])
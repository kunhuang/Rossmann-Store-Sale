from helper import *

rawStoreInfo = readCSV('store_Add0ToBlankArea.csv')
storeInfo = preprocessStoreInfo(rawStoreInfo)
promo2 = getPromo2(storeInfo[1:])
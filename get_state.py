from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
train = pd.read_csv(os.path.join('train.csv'),parse_dates=['Date'],dtype = {'StateHoliday':object})
test = pd.read_csv(os.path.join('test.csv'),parse_dates=['Date'])
# Fix StateHoliday column
train.loc[train.StateHoliday == 0,'StateHoliday'] = '0'
holid = train.loc[train.StateHoliday=='a']
bydate = holid.groupby('Date')['Store'].count()

allstores = np.unique(train.Store.values)

SN = holid.loc[holid.Date == '2013-11-20','Store'].values
BW_BY_ST = holid.loc[holid.Date == '2013-01-06','Store'].values
BW_BY_HE_NW_RP_SL = holid.loc[holid.Date == '2013-05-30','Store'].values
BW_BY_HE_NW_RP_SL = np.setxor1d(BW_BY_HE_NW_RP_SL, SN)
BY_SL = holid.loc[holid.Date =='2013-08-15','Store'].values
BB_MV_SN_ST_TH = holid.loc[holid.Date =='2013-10-31','Store'].values
BW_BY_NW_RP_SL = holid.loc[holid.Date =='2013-11-01','Store'].values
BW_BY = np.intersect1d(BW_BY_ST, BW_BY_HE_NW_RP_SL)
ST = np.setxor1d(BW_BY_ST, BW_BY)
BY = np.intersect1d(BW_BY, BY_SL)
SL = np.setxor1d(BY, BY_SL)
BW = np.setxor1d(BW_BY, BY)
HE = np.setxor1d(BW_BY_HE_NW_RP_SL,BW_BY_NW_RP_SL)
BB_MV_TH = np.setxor1d(np.setxor1d(BB_MV_SN_ST_TH,SN),ST)
NW_RP = np.setxor1d(BW_BY_NW_RP_SL,BW_BY) # SL has 0 stores
BE_HB_HH_NI_SH = np.setxor1d(np.setxor1d(allstores,BW_BY_HE_NW_RP_SL),BB_MV_SN_ST_TH)
RP = train.loc[train.Date=='2015-03-26'].loc[train.Store.isin(NW_RP)].loc[train.SchoolHoliday==1,'Store'].values
NW = np.setxor1d(NW_RP,RP)
TH = BB_MV_TH
HH = train.loc[train.Date=='2015-03-02'].loc[train.Store.isin(BE_HB_HH_NI_SH)].loc[train.SchoolHoliday==1,'Store'].values
HH1 = train.loc[train.Date=='2015-05-11'].loc[train.Store.isin(BE_HB_HH_NI_SH)].loc[train.SchoolHoliday==1,'Store'].values
BE_HB_NI_SH = np.setxor1d(BE_HB_HH_NI_SH,HH)
SH = train.loc[train.Date=='2015-04-17'].loc[train.Store.isin(BE_HB_NI_SH)].loc[train.SchoolHoliday==1,'Store'].values
SH1 = train.loc[train.Date=='2015-02-02'].loc[train.Store.isin(BE_HB_NI_SH)].loc[train.SchoolHoliday==0,'Store'].values
BE_HB_NI = np.setxor1d(BE_HB_NI_SH,SH)
BE = train.loc[train.Date=='2015-03-25'].loc[train.Store.isin(BE_HB_NI)].loc[train.SchoolHoliday==0,'Store'].values
HB_NI = np.setxor1d(BE_HB_NI,BE)

states = pd.Series('',index = allstores,name='State')
states.loc[BW] = 'BW'
states.loc[BY] = 'BY'
states.loc[BE] = 'BE'
states.loc[HB_NI] = 'HB,NI'
states.loc[HH] = 'HH'
states.loc[HE] = 'HE'
states.loc[NW] = 'NW'
states.loc[RP] = 'RP'
states.loc[SN] = 'SN'
states.loc[ST] = 'ST'
states.loc[SH] = 'SH'
states.loc[TH] = 'TH'
states[states!=''].value_counts().sum()

states.to_csv('store_states.csv', header=True, index_label='Store')
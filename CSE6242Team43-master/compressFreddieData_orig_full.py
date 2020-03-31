     # -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 12:13:57 2018

@author: DanielMower
"""

import pandas as pd
import numpy as np
# #  How To Compress Data in Pandas
# #  See: https://www.dataquest.io/blog/pandas-big-data/

# #  Get the Data:
readPath = 'C:\\Users\\DanielMower\\Desktop\\FreddieMac_SFLL_Dataset\\'
writePath = 'C:\\Users\\DanielMower\\OneDrive\\Work\\CSE_6242\Data\\'
states = ['OH'] # [Sand State, Mix Rural Urban Industrial, Rural Agricltural]
startY = 1999
startQ = 1
endY = 2017
endQ = 2
TotalQtrs = (endY-(startY+1))*4 +(4-startQ+1)+endQ # 74 # Q1 1999 through Q2 2017
saveName = 'orig_OH'


# #  Utility Functions:
# Memory Usage
def mem_usage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)

#findReplace
def findReplace(df, colname, find, replace):
    for findItem, replaceItem in zip(find,replace):
        if findItem in list(df[colname].unique()):
            df[colname].replace(findItem, replaceItem, inplace=True)
        if findItem == 'nan':
            df[colname] = df[colname].fillna(replaceItem)
    return df

#cast
def castAndDowncast(df, colname, castStr, downCast):
    if castStr == 'int': # Downcast ints to unsigned integers
        s = df[colname]
        df[colname] = s.astype(int)
        if castStr == 'unsigned':
            df[colname].apply(pd.to_numeric,downcast='unsigned')

    if castStr == 'float': # Downcast ints to unsigned integers
        s = df[colname]
        df[colname] = s.astype(float)
        if castStr == 'float':
            df[colname].apply(pd.to_numeric,downcast='float')
    
    if castStr == 'categorical':
        s = df[colname]
        df[colname] = s.astype('category')

    return df

def timeStamp_and_vintage(orig):
    s  = orig['LoanID'].str[2:4].astype(int)
    s.loc[s == 99] = 1999
    s.loc[s != 1999] = s.loc[s != 1999] + 2000
    orig['Vintage'] = s
    
    q = orig['LoanID'].str[4:6]
    orig['Orig_Qtr'] = orig.Vintage.map(str) +  q
    return orig

def timeStamp_currDate(serv):
    yr =  np.floor(serv.CurrDate/100).astype(int)
    qtr = np.ceil((serv.CurrDate - 100*np.floor(serv.CurrDate/100))/3).astype(int)
    serv['Curr_Qtr'] = yr.map(str) +  'Q'+ qtr.map(str)
    return serv

def read_orig(instructionsDictionary, ColsToKeep):
    cmbnd_df = pd.DataFrame()
    loadName = 'historical_data1_Q'
    cnt = 0
    for year in range(startY,endY+1):
        for quarter in range(1,5):
            if cnt >= TotalQtrs:
                break
            temp_df = pd.read_csv(readPath + loadName + str(quarter) + str(year) + '.txt', sep = "|", header = None)
            colDim = temp_df.shape[1]
            # #  Check Initial Memory
            print(mem_usage(temp_df))        
            
            if (colDim == 26):
                temp_df[26] = ' '
                instructionsDictionary[26] = ([None],[None],None,None,'PreHarpLoanID',False) ## 26    Pre-HARP LOAN SEQUENCE NUMBER

            temp_df.columns = temp_df.columns.map(str)
            for ii in range(len(instructionsDictionary)):
                item = instructionsDictionary[ii]
                if item[5]:
                    print(year, quarter, ii, ':', item[4])
                    temp_df = temp_df.rename(columns={str(ii): item[4]}) # Assign Column name
                    temp_df = findReplace(temp_df, item[4], item[0], item[1])
                    if item[2] != None:
                        temp_df = castAndDowncast(temp_df, item[4], item[2], item[3])
#                if not(item[5]):
#                    temp_df = temp_df.drop(item[4], 1)
            temp_df = temp_df.loc[temp_df['State'].isin(states), orig_ColsToKeep]
#            temp_df = temp_df.loc[temp_df['ZipCode'].isin(keepZips) & temp_df['State'].isin(states), orig_ColsToKeep]
            temp_df = timeStamp_and_vintage(temp_df)
            # #  Check Initial Memory
            print(mem_usage(temp_df))
            if cnt == 0:
                cmbnd_df = temp_df
            else:
                cmbnd_df = pd.concat([cmbnd_df, temp_df])
            cnt += 1   
    return cmbnd_df
# # Data Compression Instructions For Each Variable:
origDict = dict() # (find, replace, cast to, downcast to, VarName, keep = True)
origDict[0]  = (['   ', 'nan'],         [9999, 9999],   'int',          'unsigned', 'FICO',            True)  ##  0     object # CREDIT SCORE 
origDict[1]  = ([None],                 [None],         'int',          'unsigned', 'FirstPayDate',    True)  ##  1     int64 # FIRST PAYMENT DATE
origDict[2]  = ([' ', 'nan','9'],       ['U', 'U','U'], 'categorical',  None,       'FirstTimeBuyer',  True)  ##  2     object # FIRST TIME HOMEBUYER FLAG
origDict[3]  = ([None],                 [None],         'int',          'unsigned', 'MaturityDate',    True)  ##  3     int64 # MATURITY DATE
origDict[4]  = (['     ', 'nan'],       [0, 0],         'float',        'float',    'MSA',             False)  ##  4     float64 # METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION
origDict[5]  = (['000', '   ', 'nan'],  [0, 999, 999],  'int',          'unsigned', 'MInsPrcnt',       False)  ##  5     object # MORTGAGE INSURANCE PERCENTAGE (MI %)
origDict[6]  = ([' ', 'nan'],           [0, 0],         'int',          'unsigned', 'NumUnits',        False)  ##  6     float64 # NUMBER OF UNITS
origDict[7]  = ([' ', 'nan','9'],       ['U', 'U','U'], 'categorical',  None,       'OccStatus',       True)  ##  7     object # OCCUPANCY STATUS
origDict[8]  = (['nan'],                [999],          'float',        'float',    'OrigCLTV',        True)  ##  8     392771 non-null float64 # ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)
origDict[9]  = (['   ', 'nan'],         [100,999],      'float',        'float',    'OrigDTI',         True)  ##  9     376518 non-null object # ORIGINAL DEBT-TO-INCOME (DTI) RATIO - 100 now corresponts to 65+ %
origDict[10] = ([None],                 [None],         'int',          'unsigned', 'OrigBal',         True)  ## 10     int64 # ORIGINAL UPB
origDict[11] = (['   ', 'nan'],         [999, 999],     'float',        'float',    'OrigLTV',         True)  ## 11     float64 # ORIGINAL LOAN-TO-VALUE (LTV)
origDict[12] = ([None],                 [None],         None,           None,       'OrigIntRate',     True)  ## 12     float64 # ORIGINAL INTEREST RATE
origDict[13] = ([' ', 'nan','9'],       ['U', 'U','U'], 'categorical',  None,       'Channel',         False)  ## 13     object # CHANNEL
origDict[14] = ([' ', 'nan'],           ['U', 'U'],     None,           None,       'PrepayPenalty',   False)  ## 14     object # PREPAYMENT PENALTY MORTGAGE (PPM) FLAG
origDict[15] = ([None],                 [None],         'categorical',  None,       'ProdType',        True)  ## 15     object # PRODUCT TYPE
origDict[16] = ([None],                 [None],         'categorical',  None,       'State',           True)  ## 16     object # PROPERTY STATE # in  1999 there are 53 categories
origDict[17] = (['  ', 'nan','99'],     ['U', 'U','U'], 'categorical',  None,       'PropType',        True)  ## 17     object # PROPERTY TYPE
origDict[18] = (['     ', 'nan'],       [0, 0],         None,           None,       'ZipCode',         True)  ## 18     float64 # POSTAL CODE
origDict[19] = ([None],                 [None],         None,           None,       'LoanID',          True)  ## 19     object # LOAN SEQUENCE NUMBER
origDict[20] = ([' ', 'nan','9'],       ['U', 'U','U'], 'categorical',  None,       'Purpose',         True)  ## 20     object # LOAN PURPOSE
origDict[21] = ([None],                 [None],         'int',          'unsigned', 'Term',            True)  ## 21     int64 # ORIGINAL LOAN TERM
origDict[22] = (['  ', 'nan'],          [0, 0],         None,           None,       'NumBorrowers',    True)  ## 22     float64 # NUMBER OF BORROWERS
origDict[23] = ([None],                 [None],         None,           None,       'SellerName',      False) ## 23     object # SELLER NAME
origDict[24] = ([None],                 [None],         None,           None,       'ServicerName',    False) ## 24     object # SERVICER NAME
origDict[25] = (['nan',' ','Y'],        [0,0,1],        None,           None,       'SuperConforming', False)  ## 25     float64 # Super Conforming Flag

orig_ColsToKeep = list()
for key in origDict:
#    item = origDict[key]
    if origDict[key][5]:
       orig_ColsToKeep.append(origDict[key][4]) 

orig = read_orig(origDict, orig_ColsToKeep)

#Drop Nonsense Data
orig = orig.loc[(orig.FICO<= 850) & 
             (orig.OrigLTV < 999) & 
             (~orig.PropType.isin(['U'])) & 
             (orig.ZipCode >0), :]

orig.to_csv(writePath + saveName + ".txt", sep='|', index_label=False)
#orig.to_pickle(writePath + saveName + '.pkl')
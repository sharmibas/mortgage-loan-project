# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:02:59 2018

@author: DanielMower
"""

import pandas as pd
import numpy as np
# #  How To Compress Data in Pandas
# #  See: https://www.dataquest.io/blog/pandas-big-data/

# #  Get the Data:
#readPath = 'C:\\Users\\DanielMower\\Desktop\\CSE_6242\\Data\\'
readPath ='C:\\Users\\DanielMower\\Desktop\\FreddieMac_SFLL_Dataset\\'
writePath = 'C:\\Users\\DanielMower\\OneDrive\\Work\\CSE_6242\Data\\'

startY = 1999
startQ = 1
endY = 2017
endQ = 2
TotalQtrs = (endY-(startY+1))*4 +(4-startQ+1)+endQ # 74 # Q1 1999 through Q2 2017
saveName = 'perf_OH'
origFileName = 'orig_OH'


# #  Utility Functions:
# Memory Usage
def mem_usage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)

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

def timeStamp_currDate(serv):
    yr =  np.floor(serv.CurrDate/100).astype(int)
    qtr = np.ceil((serv.CurrDate - 100*np.floor(serv.CurrDate/100))/3).astype(int)
    serv['Curr_Qtr'] = yr.map(str) +  'Q'+ qtr.map(str)
    return serv

def willDefaultWithinNPeriods(df, n_periods, newVarName, deletePast_default_Flag):
    keepCols = list(df.columns) + [newVarName]
    df["willHappenIn2_step1"] = df.dflt.groupby(df['LoanID']).cumsum().astype(int)
    df["willHappenIn2_step2"] = df.willHappenIn2_step1.groupby(df['LoanID']).cumsum().astype(int)
    df["willHappenIn2_step3"] = df.willHappenIn2_step2
    df.loc[df.willHappenIn2_step2>1,"willHappenIn2_step3"] = -1
    df[newVarName] = df["willHappenIn2_step3"].groupby(df.LoanID).apply( lambda x: x.replace(to_replace=0, method='bfill', limit = n_periods))    
    
   
    if deletePast_default_Flag:
        df = df.loc[df[newVarName]>=0,keepCols]
    else:
        df = df.loc[:,keepCols]
    return df 

def read_perf(instructionsDictionary, ColsToKeep, uniqueIDs):
    cmbnd_df = pd.DataFrame()
    loadName = 'historical_data1_time_Q'
    cnt = 0
    for year in range(startY,endY+1):
        for quarter in range(1,5):
            if cnt >= TotalQtrs:
                break
            temp_df = pd.read_csv(readPath + loadName + str(quarter) + str(year) + '.txt', sep = "|", header = None)
            # #  Check Initial Memory
            print(mem_usage(temp_df))        
            temp_df.columns = temp_df.columns.map(str)
            for ii in range(len(instructionsDictionary)):
                item = instructionsDictionary[ii]
                if item[5]:
                    if ii > 0:
                        temp_df = temp_df.loc[temp_df['LoanID'].isin(uniqueIDs),:]
                    if item[4] in ColsToKeep:
                        print(year, quarter, ii, ':', item[4])
                        temp_df = temp_df.rename(columns={str(ii): item[4]}) # Assign Column name
                        temp_df = findReplace(temp_df, item[4], item[0], item[1])
                        if item[2] != None:
                            temp_df = castAndDowncast(temp_df, item[4], item[2], item[3])
                    else:
                        temp_df = temp_df.drop(str(ii), 1)
            ##  Check Initial Memory
            print(mem_usage(temp_df))
             
            # Fix Issue with some CurrDates
            temp_df.loc[temp_df.CurrDate < 2025,['CurrDate']] = temp_df.loc[temp_df.CurrDate < 2025,['CurrDate']]*100
            temp_df = timeStamp_currDate(temp_df)
            
            if cnt == 0:
                cmbnd_df = temp_df
            else:
                cmbnd_df = pd.concat([cmbnd_df, temp_df])
            cnt += 1   
    return cmbnd_df


orig = pd.read_csv(writePath + origFileName + ".txt", sep='|')

IDs = list(orig['LoanID'].unique())
del orig # Free up working memory

perfDict = dict() # (find, replace, cast to, downcast to, VarName, keep = True)
perfDict[0]  = ([None],                 [None],             None,           None,           'LoanID',               True)  ##  0     LOAN SEQUENCE NUMBER
perfDict[1]  = ([None],                 [None],             'int',          'unsigned',     'CurrDate',             True)  ##  1     MONTHLY REPORTING PERIOD
perfDict[2]  = ([None],                 [None],             'int',          'unsigned',     'CurrBal',              True)  ##  2     CURRENT ACTUAL UPB
perfDict[3]  = (['R','   ','nan','XX'], [998,999,999,999],  'int',          'unsigned',     'Status',               True)  ##  3     CURRENT LOAN DELINQUENCY STATUS
perfDict[4]  = ([None],                 [None],             'int',          'unsigned',     'Age',                  True)  ##  4     LOAN AGE
perfDict[5]  = ([None],                 [None],             'int',          'unsigned',     'MonthsToMaturity',     True)  ##  5     REMAINING MONTHS TO LEGAL MATURITY
perfDict[6]  = ([' ', 'nan'],           ['U', 'U'],         'categorical',  None,           'RepoFlag',             True)  ##  6     REPURCHASE FLAG
perfDict[7]  = ([' ', 'nan'],           ['N', 'N'],         'categorical',  None,           'ModFlag',              True)  ##  7     MODIFICATION FLAG
perfDict[8]  = (['  ', 'nan'],          [99,99],            'categorical',  None,           'ZeroBalCode',          True)  ##  8     ZERO BALANCE CODE
perfDict[9]  = (['      ','nan'],       [0,0],              'int',          'unsigned',     'ZeroBalDate',          True)  ##  9     ZERO BALANCE EFFECTIVE DATE
perfDict[10] = ([None],                 [None],             'int',          'unsigned',     'CurrIntRate',          True)  ## 10     CURRENT INTEREST RATE
perfDict[11] = (['   ', 'nan'],         [999, 999],         'int',          'unsigned',     'CurrDeferredBal',      False)  ## 11     CURRENT DEFERRED UPB
perfDict[12] = (['nan'],                [0],                'int',          'unsigned',     'DDLPI',                False)  ## 12     DUE DATE OF LAST PAID INSTALLMENT (DDLPI)
perfDict[13] = (['nan'],                [0],                'int',          'unsigned',     'MInsRecs',             False)  ## 13     MI RECOVERIES
perfDict[14] = (['nan','U','C'],        [0, 0, 9999999],     None,          None,           'NetSalesPrcds',        False)  ## 14     NET SALES PROCEEDS
perfDict[15] = (['nan'],                [0],                'int',          None,           'NonMInsRecs',          False)  ## 15     NON MI RECOVERIES -  Values of 'C' are going to be set to 999999 and later changed to UPB (this leaves out delinquent accrued interest)
perfDict[16] = (['nan'],                [0],                'int',          None,           'Expenses',             False)  ## 16     EXPENSES
perfDict[17] = (['nan'],                [0],                'int',          None,           'LegalCosts',           False)  ## 17     Legal Costs
perfDict[18] = (['nan'],                [0],                'int',          None,           'MaintPresCosts',       False)  ## 18     Maintenance and Preservation Costs
perfDict[19] = (['nan'],                [0],                'int',          None,           'TaxIns',               False)  ## 19     Taxes and Insurance
perfDict[20] = (['nan'],                [0],                'int',          None,           'MiscExpenses',         False)  ## 20     Miscellaneous Expenses
perfDict[21] = (['nan'],                [0],                'int',          None,           'ActLossCalc',          False)  ## 21     Actual Loss Calculation
perfDict[22] = (['nan'],                [0],                'float',        'float',        'ModCost',              False)  ## 22     Modification Cost

serv_ColsToKeep = list()
for key in perfDict:
#    item = origDict[key]
    if perfDict[key][5]:
       serv_ColsToKeep.append(perfDict[key][4]) 

serv = read_perf(perfDict, serv_ColsToKeep, IDs)

#Drop Nonsense Data
serv = serv.loc[(serv.ZeroBalCode<= 99) & 
             (serv.Status < 999) & 
             (serv.CurrIntRate < 20), :]

#Add/Alter The following Variables3
# Default within 1-year 'dflt1'
#          Will have a 1 for each date within 12-months of the default date.
serv = serv.sort_values(['LoanID','CurrDate'], ascending=[True,True])
serv['dflt'] = np.zeros(serv.shape[0])
serv.loc[(serv.ZeroBalCode.isin([3,9])) | ((serv.Status >= 4) & (serv.Status <= 998)),['dflt']] = 1
serv = willDefaultWithinNPeriods(serv, 11, 'dflt1', True)

#ModFlag  - Turn it into and on-switch.  Once a modification happens it stays on.  If another happens
#           The switch turns to 2 from that point forward ...
serv = serv.sort_values(['LoanID','CurrDate'], ascending=[True,True])
serv.ModFlag = serv.ModFlag.eq('Y', fill_value=0).astype(int)
serv["NumModsToDate"] = serv.ModFlag
serv.NumModsToDate = serv.ModFlag.groupby(serv['LoanID']).cumsum()

# Create a Pre-PaymentFlag
#           On the date of Prepayment incicate a 1 and 0 otherwise.
serv["PrePayFlag"] = 0
serv.loc[serv.ZeroBalCode == 1, "PrePayFlag"] = 1

#serv.to_pickle(writePath + saveName + '.pkl')
serv.to_csv(writePath + saveName + ".txt", sep='|', index_label=False)

#Add DFLT and PREPAY to orig data
dfltIDs = list(serv.loc[serv['dflt']==1,'LoanID'].unique())
prepayIDS = list(serv.loc[serv['PrePayFlag']==1,'LoanID'].unique())
orig = pd.read_csv(writePath + origFileName + ".txt", sep='|')
orig['DFLT'] = 0
orig['PREPAY'] = 0
orig.loc[orig.LoanID.isin(dfltIDs),'DFLT'] = 1
orig.loc[orig.LoanID.isin(prepayIDS),'PREPAY'] = 1
orig.to_csv(writePath + origFileName + ".txt", sep='|', index_label=False)

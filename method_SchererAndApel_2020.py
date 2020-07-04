"""
Name:Identification of phases based on method by Scherer and Apel (2020)
Author: Jinkai Zhang
Date: July 6, 2020

Description:
    The approach is an enhancement of the economic model developed by Vliet and Blitz (2011) as the methodology is intuitive, robust, and easily applicable.
    Aggregated Z-scores calculated from different series.
    E.g. Expansion: Z-score positive and increasing.

Phases Identification:
    4-phases: Method consistent with Scherer and Apel (2020)
    2-phases: An simple extension
    6-phases: Developed by JR:
        Reference: https://github.com/ClearMacroIPD/MHF/blob/master/NOWCASTING/MIDASMODEL.py

Single Indicator:
    OECD Component Leading Index(CLI):
        The components of the CLI are time series which exhibit leading relationship with the reference series (GDP) at turning points. 
        Reference: https://www.oecd.org/sdd/compositeleadingindicatorsclifrequentlyaskedquestionsfaqs.htm

Multiple Indicators (Scherer and Apel, 2020):
    A composite Z-score index combined by:
        1. U.S. unemployment rate;
        2. Producer sentiment: Markit Global Manufacturing PMI (MPMIGLMA Index) and ISM Non-Manufacturing NMI (NAPMNMI Index);
        3. Consumer sentiment: The Conference Board Consumer Confidence Index (CONCCONF Index, PURCHASE NEEDED) and the University of Michigan Consumer Sentiment Index (CONSSENT Index);
        4. Financial market stress : Kansas City Financial Stress Index (KCFSINDX Index)
        5. Economic growth: OECD CLI Index
        Note: 
            The inverse of the unemployment rate and the financial stress indicator with the opposite sign are used for further analysis.
            Each of the five dimensions contributes equally to the overall regime indicator.
            To limit the influence of individual variables we cap the Z-score to three standard deviations on either side.

Avoid Look-ahead bias:
    The Z-scores are calculated at the end of each month under the expanding window (at least 3-years) approach.

Reference:
    Scherer, B. and Apel, M., 2020. Business Cycle–Related Timing of Alternative Risk Premia Strategies. Journal of Alternative Investments, 22 (4), 8-24.
    Vliet, P.V., and Blits, D., 2011. Dynamic strategic asset allocation: Risk and return across the business cycle. Journal of Asset Management, 12, 360-375.

"""

import pandas as pd
import numpy as np
import random
from datetime import datetime


#last day in month

LastDay_Leap = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
LastDay_NonLeap = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

#Data load
#Phase Identification with SINGLE serie-OECD data
ALL_CLI = pd.read_csv('Data/OECD.csv')
OECD_CLI = ALL_CLI[ALL_CLI.LOCATION == 'OECD'][['TIME', 'Value']]

#Phase Identification with MULTIPLE series, see Scherer and Apel (2020) in detail
CONSSENT = pd.read_csv('Data/CONSSENT.csv') #Consumer sentiment2: University of Michigan Consumer Sentiment Index
KCFSINDX = pd.read_csv('Data/KCFSINDX.csv') #Financial market stress : Kansas City Financial Stress Index

#Given different data has different date format, these functions are to make them consistent

def Reform_OECD (df):
    try:
        df.index = range(len(df))
        for i in range(len(df)):
            date = datetime.strptime(df['TIME'][i], '%Y-%m')
            year = date.year
            month = date.month         
            if year % 4 == 0:
                df['TIME'][i] = str(df['TIME'][i]) + "-" + str(LastDay_Leap[month])
            else:
                df['TIME'][i] = str(df['TIME'][i]) + "-" + str(LastDay_NonLeap[month])
        df.columns = ['Date', 'Index']
        return df   
    except:
        print("This function can be only run once, please reload the data and run it once.")

OECD_CLI = Reform_OECD(OECD_CLI)

def Reform_CONSSENT (df):
    try:
        for i in range(len(df)):
            if df['Month'][i] < 10:
                month_str = "0" + str(df['Month'][i])
            else:
                month_str = str(df['Month'][i])
            if df['Year'][i] % 4 == 0:
                df['Year'][i] = str(df['Year'][i]) + "-" + month_str + "-" + str(LastDay_Leap[df['Month'][i]])
            else:
                df['Year'][i] = str(df['Year'][i]) + "-" + month_str + "-" + str(LastDay_NonLeap[df['Month'][i]])
        df =  df.drop('Month', axis = 1)
        df.columns = ['Date', 'Index']
        return df
    except:
        print("This function can be only run once, please reload the data and run it once.")

CONSSENT = Reform_CONSSENT(CONSSENT)

def Reform_KCFSINDX (df):
    try:
        for i in range(len(df)):
            date = datetime.strptime(df['DATE'][i], '%Y-%m-%d')
            year = date.year
            month = date.month
            if month < 10:
                month_str = "0" + str(month)
            else:
                month_str = str(month)
            if year % 4 == 0:
                df['DATE'][i] = str(year) + "-" + month_str + "-" + str(LastDay_Leap[month])
            else:
                df['DATE'][i] = str(year) + "-" + month_str + "-"  + str(LastDay_NonLeap[month])
        df.columns = ['Date', 'Index']
        return df
    except:
        print("This function can be only run once, please reload the data and run it once.")
    
        
KCFSINDX = Reform_KCFSINDX(KCFSINDX)

# In order to avoid look-ahead bias, we do not use the existing package of calculation of Z-score
def Get_Zscore (df, rolling_year = 3):
    rolling_month = rolling_year * 12
    zscore = [np.nan for i in range(rolling_month - 1)]
    for i in range(rolling_month - 1, len(df)):
        start_index = i - rolling_month + 1
        end_index = i
        series = df['Index'][start_index : end_index + 1]
        mean_rolling = series.mean()
        std_rolling = series.std()
        index_current = df['Index'][i]
        upper_cap, lower_cap = (mean_rolling + 3 * std_rolling), (mean_rolling - 3 * std_rolling)
        if index_current > upper_cap:
            index_current = upper_cap
        elif index_current < lower_cap:
            index_current = lower_cap
        else:
            pass
        zscore_current = (index_current - mean_rolling) / std_rolling
        zscore.append(zscore_current)
    df['Z_Score'] = zscore
    return df


def Get_Zscore_Inverse (df, rolling_year = 3):
    df = Get_Zscore (df, rolling_year)
    df['Z_Score'] = -1 * df['Z_Score']
    return df

OECD_CLI_Zscore = Get_Zscore(OECD_CLI)
CONSSENT_Zscore = Get_Zscore(CONSSENT)
# financial stress index below has to be inversed in calculation of signals
KCFSINDX_Zscore = Get_Zscore_Inverse(KCFSINDX)

def Ger_Zscore_Composite (df1, df2, df3):
    df1.index = df1['Date']
    df1 = df1.drop(['Date', 'Index'], axis = 1)
    df1.columns = ['Z1']
    df2.index = df2['Date']
    df2 = df2.drop(['Date', 'Index'], axis = 1)
    df2.columns = ['Z2']
    df3.index = df3['Date']
    df3 = df3.drop(['Date', 'Index'], axis = 1)
    df3.columns = ['Z3']
    df = [df1, df2, df3]
    df = pd.concat(df, axis = 1)
    df = df.dropna()
    df['Z_Composite'] = df['Z1']/3 + df['Z2']/3 +df['Z3']/3
    return df

Composite_Zscore = Ger_Zscore_Composite(OECD_CLI_Zscore, CONSSENT_Zscore, KCFSINDX_Zscore)

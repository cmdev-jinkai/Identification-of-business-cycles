"""
Name:Identification of phases based on method by Scherer and Apel (2020)
Author: Jinkai Zhang
Date: July 6, 2020

Algorithm of Six Phases Identification provided by Jean Ricaume:
    Reference: https://github.com/ClearMacroIPD/MHF/blob/master/MTR/CYCLE/PHASES.py

Description:
    The approach is an enhancement of the economic model developed by Vliet and Blitz (2011) as the methodology is intuitive, robust, and easily applicable.
    Aggregated Z-scores calculated from different series.
    E.g. Expansion: Z-score positive and increasing.

Phases Identification:
    4-phases: Method consistent with Scherer and Apel (2020)
    2-phases: An simple extension
    6-phases: Proposed and developed by JR:
        Reference: https://github.com/ClearMacroIPD/MHF/blob/master/MTR/CYCLE/PHASES.py

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
from PHASES_in_Six_JR import get_cycle_phase

#last day in month

LastDay_Leap = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
LastDay_NonLeap = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

#Data load
#Phase Identification with SINGLE serie-OECD data
ALL_CLI = pd.read_csv('Data/OECD.csv')
OECD_CLI = ALL_CLI[ALL_CLI.LOCATION == 'OECD'][['TIME', 'Value']]

#Phase Identification with MULTIPLE series, see Scherer and Apel (2020) in detail FIVE DIMENTION
CONSSENT = pd.read_csv('Data/CONSSENT.csv') #Consumer sentiment2: University of Michigan Consumer Sentiment Index
KCFSINDX = pd.read_csv('Data/KCFSINDX.csv') #Financial market stress : Kansas City Financial Stress Index
#OECD_CLI also included here
UNEMPLOY = pd.read_csv('Data/UNEMPLOY.csv') #U.S. enemployment rate
ISMMANU =  pd.read_csv('Data/ISMMANU.csv') #produce sentiment; ISM Manufactory index


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

def Reform_UNEMPLOY (df):
    try:
        df.index = range(len(df))
        for i in range(len(df)):
            date = datetime.strptime(df['Date'][i], '%m/%d/%Y')
            year = date.year
            month = date.month
            if month < 10:
                month_str = "0" + str(month)
            else:
                month_str = str(month)
            if year % 4 == 0:
                df['Date'][i] = str(year) + "-" + month_str + '-' + str(LastDay_Leap[month])
            else:
                df['Date'][i] = str(year) + "-" + month_str + '-' + str(LastDay_NonLeap[month])
        df.columns = ['Date', 'Index']
        return df   
    except:
        print("This function can be only run once, please reload the data and run it once.")

def Reform_ISMMANU (df):
    try:
        df.index = range(len(df))
        for i in range(len(df)):
            date = datetime.strptime(df['Date'][i], '%m/%d/%Y')
            year = date.year
            month = date.month
            if month < 10:
                month_str = "0" + str(month)
            else:
                month_str = str(month)
            if year % 4 == 0:
                df['Date'][i] = str(year) + "-" + month_str + '-' + str(LastDay_Leap[month])
            else:
                df['Date'][i] = str(year) + "-" + month_str + '-' + str(LastDay_NonLeap[month])
        df.columns = ['Date', 'Index']
        return df   
    except:
        print("This function can be only run once, please reload the data and run it once.")

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
    
        


# Calculate Z-score in the framework of single input(OECD) without cap the 3 standard deviation
def Get_Zscore_NoCap (df, rolling_year = 3):
    rolling_month = rolling_year * 12
    zscore = [np.nan for i in range(rolling_month - 1)]
    for i in range(rolling_month - 1, len(df)):
        start_index = i - rolling_month + 1
        end_index = i
        series = df['Index'][start_index : end_index + 1]
        mean_rolling = series.mean()
        std_rolling = series.std()
        index_current = df['Index'][i]
        zscore_current = (index_current - mean_rolling) / std_rolling
        zscore.append(zscore_current)
    df['Z_Score'] = zscore
    df = df.dropna()
    return df



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
    df = df.dropna()
    return df


def Get_Zscore_Inverse (df, rolling_year = 3):
    df = Get_Zscore (df, rolling_year)
    df['Z_Score'] = -1 * df['Z_Score']
    return df


def Ger_Zscore_Composite (df1, df2, df3, df4, df5):
    df1.index = df1['Date']
    df1 = df1.drop(['Date', 'Index'], axis = 1)
    df1.columns = ['Z1']
    df2.index = df2['Date']
    df2 = df2.drop(['Date', 'Index'], axis = 1)
    df2.columns = ['Z2']
    df3.index = df3['Date']
    df3 = df3.drop(['Date', 'Index'], axis = 1)
    df3.columns = ['Z3']
    df4.index = df4['Date']
    df4 = df4.drop(['Date', 'Index'], axis = 1)
    df4.columns = ['Z4']
    df5.index = df5['Date']
    df5 = df5.drop(['Date', 'Index'], axis = 1)
    df5.columns = ['Z5']
    df = [df1, df2, df3, df4, df5]
    df = pd.concat(df, axis = 1)
    df = df.dropna()
    df['Z_Composite'] = df['Z1']/5 + df['Z2']/5 + df['Z3']/5 + df['Z4']/5 + df['Z5']/5
    df.insert(loc = 0, column='Date', value = df.index)
    return df


def Identify_Phase (df_Single, df_Multiple, Series_Type, Number_Phase):   
    if Series_Type == 'Single': #use OECD Z-score
        #Initialize the data
        df_Single = Get_Zscore_NoCap(OECD_CLI)
        if Number_Phase == 2:
            Phase = []
            for i in range(len(df_Single)):
                zscore_current = df_Single.iloc[i]['Z_Score']
                if zscore_current >= 0:
                    Phase.append('expansion')
                else:
                    Phase.append('contraction')
            df_Single['phase'] = Phase
            return df_Single
        elif Number_Phase == 4:
            Phase = [np.nan]
            for i in range(1, len(df_Single)):
                zscore_current = df_Single.iloc[i]['Z_Score']
                zscore_last =  df_Single.iloc[i-1]['Z_Score']
                if zscore_current >= 0 and zscore_current >= zscore_last:
                    Phase.append('expansion')
                elif zscore_current >= 0 and zscore_current < zscore_last:
                    Phase.append('slowdown')
                elif zscore_current <= 0 and zscore_current >= zscore_last:
                    Phase.append('recovery')
                else:
                    Phase.append('contraction')
            df_Single['phase'] = Phase
            df_Single = df_Single.dropna()
            return df_Single
        elif Number_Phase == 6:
            # switch the Z_Score to the first column to be consistent with the 6 phase function
            df_Single['Z_Score'], df_Single['Date'] = df_Single['Date'], df_Single['Z_Score']
            df_Single = get_cycle_phase(df_Single, model = 'MA', window = 8, thresh = 0)
            # swith back
            df_Single['Z_Score'], df_Single['Date'] = df_Single['Date'], df_Single['Z_Score']
            return df_Single
        else:
            print('The number of phases is not included in the framework')
    elif Series_Type == 'Multiple': # use composite Z-score
        #Initialize the data
        OECD_CLI_Zscore = Get_Zscore(OECD_CLI)
        CONSSENT_Zscore = Get_Zscore(CONSSENT)
        KCFSINDX_Zscore = Get_Zscore_Inverse(KCFSINDX)
        UNEMPLOY_Zscore = Get_Zscore_Inverse(UNEMPLOY)
        ISMMANU_Zscore = Get_Zscore(ISMMANU)
        df_Multiple = Ger_Zscore_Composite(OECD_CLI_Zscore, CONSSENT_Zscore, KCFSINDX_Zscore, UNEMPLOY_Zscore, ISMMANU_Zscore)
        if Number_Phase == 2:
            Phase = []
            for i in range(len(df_Multiple)):
                zscore_current = df_Multiple.iloc[i]['Z_Composite']
                if zscore_current >= 0:
                    Phase.append('expansion')
                else:
                    Phase.append('contraction')
            df_Multiple['phase'] = Phase
            return df_Multiple
        elif Number_Phase == 4:
            Phase = [np.nan]
            for i in range(1, len(df_Multiple)):
                zscore_current = df_Multiple.iloc[i]['Z_Composite']
                zscore_last =  df_Multiple.iloc[i-1]['Z_Composite']
                if zscore_current >= 0 and zscore_current >= zscore_last:
                    Phase.append('expansion')
                elif zscore_current >= 0 and zscore_current < zscore_last:
                    Phase.append('slowdown')
                elif zscore_current <= 0 and zscore_current > zscore_last:
                    Phase.append('recovery')
                else:
                    Phase.append('contraction')
            df_Multiple['phase'] = Phase
            df_Multiple = df_Multiple.dropna()
            return df_Multiple
        elif Number_Phase == 6:
            # switch the Z_Composite to the first column to be consistent with the 6 phase function
            df_Multiple['Z_Composite'], df_Multiple['Date'] = df_Multiple['Date'], df_Multiple['Z_Composite']
            df_Multiple = get_cycle_phase(df_Multiple, model = 'MA', window = 8, thresh = 0)
            # swith back
            df_Multiple['Z_Composite'], df_Multiple['Date'] = df_Multiple['Date'], df_Multiple['Z_Composite']
            return df_Multiple
        else:
            print('The number of phases is not included in the framework') 
    else:
        print('Please check the spelling of input.')

if __name__ == '__main__':
    
    #To make the date format consistent with %Y-%m-%d
    OECD_CLI = Reform_OECD(OECD_CLI)
    CONSSENT = Reform_CONSSENT(CONSSENT)
    KCFSINDX = Reform_KCFSINDX(KCFSINDX)
    UNEMPLOY = Reform_UNEMPLOY(UNEMPLOY)
    ISMMANU = Reform_ISMMANU(ISMMANU)
    
    #OECD Z_score in SINGLE input framework
    OECD_Single_Zscore = Get_Zscore_NoCap(OECD_CLI)

    #OECD Z_score in MULTIPLE input framework
    OECD_CLI_Zscore = Get_Zscore(OECD_CLI)
    CONSSENT_Zscore = Get_Zscore(CONSSENT)
    #Note: financial stress index below has to be inversed in calculation of signals
    KCFSINDX_Zscore = Get_Zscore_Inverse(KCFSINDX)
    UNEMPLOY_Zscore = Get_Zscore_Inverse(UNEMPLOY)
    ISMMANU_Zscore = Get_Zscore(ISMMANU)
    #Composite Zscore: MORE SERIES TO BE ADDED
    Composite_Zscore = Ger_Zscore_Composite(OECD_CLI_Zscore, CONSSENT_Zscore, KCFSINDX_Zscore, UNEMPLOY_Zscore, ISMMANU_Zscore)
   
    '''
    Correlation Matrix
    Z1: Economic Growth - OECD CLI Index
    Z2: Consumer Sentiment - University of Michigan Consumer Sentiment Index 
    Z3: Financial Stress - Kansas City Financial Stress Index
    Z4: Unemployment Rate - U.S. unemployment rate;
    Z5: Producer Sentiment - ISM factor (ISM manufacturers’ survey production index);

    
    # Composite_Zscore.iloc[:, 1:6].corr()
    
              Z1        Z2        Z3        Z4        Z5
        Z1  1.000000  0.461546  0.375933  0.502463  0.677101
        Z2  0.461546  1.000000  0.265916  0.632296  0.473199
        Z3  0.375933  0.265916  1.000000  0.110936  0.458854
        Z4  0.502463  0.632296  0.110936  1.000000  0.187146
        Z5  0.677101  0.473199  0.458854  0.187146  1.000000
    
    '''
    
    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ Outputs ~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """

    SingleInput_2Phases = Identify_Phase(OECD_Single_Zscore, Composite_Zscore, 'Single', 2)
    SingleInput_2Phases.tail(20)
    SingleInput_4Phases = Identify_Phase(OECD_Single_Zscore, Composite_Zscore, 'Single', 4)
    SingleInput_4Phases.tail(20)
    SingleInput_6Phases = Identify_Phase(OECD_Single_Zscore, Composite_Zscore, 'Single', 6)
    SingleInput_6Phases.tail(20)
    
    #run it when to get the OECD data since 1993
    #SingleInput_2Phases = SingleInput_2Phases.iloc[len(SingleInput_2Phases) - 329 : len(SingleInput_2Phases), :]
    #SingleInput_4Phases = SingleInput_4Phases.iloc[len(SingleInput_4Phases) - 329 : len(SingleInput_4Phases), :]
    #SingleInput_6Phases = SingleInput_6Phases.iloc[len(SingleInput_6Phases) - 329 : len(SingleInput_6Phases), :]
    
    
    
    
    MultipleInput_2Phases = Identify_Phase(OECD_Single_Zscore, Composite_Zscore, 'Multiple', 2)
    MultipleInput_2Phases.tail(20)
    MultipleInput_4Phases = Identify_Phase(OECD_Single_Zscore, Composite_Zscore, 'Multiple', 4)
    MultipleInput_4Phases.tail(20)
    MultipleInput_6Phases = Identify_Phase(OECD_Single_Zscore, Composite_Zscore, 'Multiple', 6)
    MultipleInput_6Phases.tail(20)





    



















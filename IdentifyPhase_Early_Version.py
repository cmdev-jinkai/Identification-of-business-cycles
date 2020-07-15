'''
Name:Identification of cycles with different number of phases
Author: Jinkai Zhang
Date: June 23, 2020
Description:
    This file provides the functions to identify the business cycles while allowing users to choose the number of total cycles
    The methods are application to the other time series data in the identification of cycles
    There are three types of phases identification included which are:
        Two phases identication: 'Expansion', 'Recession'
        Four phases identification: "Expansion", "Slowdown","Recession", "Recovery"
        Six phases identification: "Expansion", "Slowdown","Recession", "Recovery", "DoubleUp", "DoubleDown"
    
Logic of the idenfication in Two phases:
    1. Two phases identification is straightford depending on whether the index above/below mean (e.g. 100 in OECD data)
    
Logic of the idenfication in Four phases:
    1. Identify all the peaks with the mark of '+' and '-' representing up and down peak
    2. In time series data, if two or more consecutive '+'/'-' peak identified, we choose the most evident peak, allowing up and down peak appears alternatively
    3. Use the time point of peak and whether it is above mean to determine the position of cycle

Logic of the idenfication in Six phases:
    1. logis of six phases are based on four phase;
    2. In point 2 of logic to identify four phase, if two consecutive '+' are observed as peak, the period in these two shall be identified as 'DoubleUp' phase
    3. Similar application to 'DoubleDown' phase
    4. adjust the existing months in four phase
'''

import pandas as pd
import numpy as np
import random
from datetime import datetime

ALL_CLI = pd.read_csv('Data/OECD.csv')
OECD_CLI = ALL_CLI[ALL_CLI.LOCATION == 'OECD'][['TIME', 'Value']]

#SP_return = pd.read_csv('sp_price.csv')


def Identify_All_Peak (df):
    df_peak = pd.DataFrame(columns = ["Date", "Value", "Direction"])
    date_peak, value_peak, direction_peak = [], [], []
    for i in range(1, len(df) - 1):
        if df.iloc[i]['Value'] > 100 and df.iloc[i]['Value'] >= df.iloc[i-1]['Value'] and df.iloc[i]['Value'] >= df.iloc[i+1]['Value']:
            date_peak.append(df.iloc[i]['TIME'])
            value_peak.append(df.iloc[i]['Value'])
            direction_peak.append('+')
        elif df.iloc[i]['Value'] < 100 and df.iloc[i]['Value'] <= df.iloc[i-1]['Value'] and df.iloc[i]['Value'] <= df.iloc[i+1]['Value']:
            date_peak.append(df.iloc[i]['TIME'])
            value_peak.append(df.iloc[i]['Value'])
            direction_peak.append('-')
    df_peak = df_peak.append(pd.DataFrame({"Date":date_peak,"Value":value_peak, "Direction":direction_peak})) 
    return df_peak


def Identify_Peak_FourPhases (df_peak):
    i = 0
    while True:
        if i < len(df_peak):
            if df_peak.iloc[i]['Direction'] == df_peak.iloc[i-1]['Direction']:
                if df_peak.iloc[i]['Direction'] == "+":
                    if df_peak.iloc[i]['Value'] > df_peak.iloc[i-1]['Value']:
                        df_peak = df_peak.drop(df_peak.index[i-1])
                    else:
                        df_peak = df_peak.drop(df_peak.index[i])
                elif df_peak.iloc[i]['Direction'] == "-":
                    if df_peak.iloc[i]['Value'] < df_peak.iloc[i-1]['Value']:
                        df_peak = df_peak.drop(df_peak.index[i-1])
                    else:
                        df_peak = df_peak.drop(df_peak.index[i])
            else:
                i += 1
        else:
            return df_peak  
        

def Identify_Phase (Number_Phase, df):
    if Number_Phase == 2:
        phase1, phase2 = "Expansion", "Recession"
        month1, month2 = [], []
        Output = dict()
        for i in range(len(df)):
            if df.iloc[i]['Value'] >= 100:
                month1.append(df.iloc[i]['TIME'])
            else:
                month2.append(df.iloc[i]['TIME'])
        Output[phase1], Output[phase2] = month1, month2
        return Output
    elif Number_Phase == 4:
        phase1, phase2, phase3, phase4 = "Expansion", "Slowdown","Recession", "Recovery"
        month1, month2, month3, month4 = [], [], [], []
        Output = dict()
        df_four = Identify_Peak_FourPhases(Identify_All_Peak(df))
        df.index = range(len(df))
        df_four.index = range(len(df_four))
        past_index = 0
        i = 0
        while True:
            if i != len(df_four) - 1:
                current_peakday = df_four.iloc[i]['Date']
                current_index = df[df.TIME == current_peakday].index.tolist()[0]
                for j in range(past_index, current_index + 1):
                    if df_four.iloc[i]['Direction'] == '+':
                        if df.iloc[j]['Value'] >= 100:
                            month1.append(df.iloc[j]['TIME'])
                        else:
                            month4.append(df.iloc[j]['TIME'])
                    else:
                        if df.iloc[j]['Value'] >= 100:
                            month2.append(df.iloc[j]['TIME'])
                        else:
                            month3.append(df.iloc[j]['TIME'])
                past_index = current_index + 1
                i += 1
            else:
                current_peakday = df_four.iloc[i]['Date']
                current_index = df[df.TIME == current_peakday].index.tolist()[0]
                for j in range(current_index + 1, len(df)):
                    if df_four.iloc[i]['Direction'] == '+':
                        if df.iloc[j]['Value'] >= 100:
                            month2.append(df.iloc[j]['TIME'])
                        else:
                            month3.append(df.iloc[j]['TIME'])
                    else:
                        if df.iloc[j]['Value'] >= 100:
                            month4.append(df.iloc[j]['TIME'])
                        else:
                            month1.append(df.iloc[j]['TIME'])
                Output[phase1], Output[phase2] = month1, month2
                Output[phase3], Output[phase4] = month3, month4
                return Output
    elif Number_Phase == 6:
        Output = Identify_Phase(4, df)
        phase5, phase6 = "DoubleUp", "DoubleDown"
        month5, month6 = [], []
        df_six = Identify_All_Peak(df)
        df.index = range(len(df))
        df_six.index = range(len(df_six))
        for i in range(len(df_six) - 1):
            if df_six.iloc[i]['Direction'] == df_six.iloc[i+1]['Direction']:
                begin_month = df_six.iloc[i]['Date']
                end_month = df_six.iloc[i+1]['Date']
                begin_index = df[df.TIME == begin_month].index.tolist()[0]
                end_index = df[df.TIME == end_month].index.tolist()[0]           
                if df_six.iloc[i]['Direction'] == '+':
                    for j in range(begin_index + 1, end_index):
                        month5.append(df.iloc[j]['TIME'])
                else:
                    for j in range(begin_index + 1, end_index):
                        month6.append(df.iloc[j]['TIME'])
        Output[phase5] = month5
        Output[phase6] = month6
        double_month = month5 + month6
        Output['Expansion'] = np.setdiff1d(Output['Expansion'], double_month).tolist()
        Output['Slowdown'] = np.setdiff1d(Output['Slowdown'], double_month).tolist()
        Output['Recession'] = np.setdiff1d(Output['Recession'], double_month).tolist()
        Output['Recovery'] = np.setdiff1d(Output['Recovery'], double_month).tolist()
        return Output
        
        
if __name__ == '__main__':
    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ EXAMPLES ~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    TwoPhases_Collection = Identify_Phase(2, OECD_CLI)
    TwoPhases_Collection.keys()
    print(TwoPhases_Collection['Expansion'])
    FourPhases_Collection = Identify_Phase(4, OECD_CLI)
    FourPhases_Collection.keys()
    print(FourPhases_Collection['Recovery'])
    SixPhases_Collection = Identify_Phase(6, OECD_CLI)
    SixPhases_Collection.keys()
    print(SixPhases_Collection['DoubleUp'])
    























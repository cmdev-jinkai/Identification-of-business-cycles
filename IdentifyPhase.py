import pandas as pd
import numpy as np
import random
from datetime import datetime

ALL_CLI = pd.read_csv('OECD.csv')
OECD_CLI = ALL_CLI[ALL_CLI.LOCATION == 'OECD'][['TIME', 'Value']]

SP_return = pd.read_csv('sp_price.csv')

#first_time = datetime.strptime(df.iloc[0]['TIME'], '%Y-%m')
#last_time = datetime.strptime(df.iloc[len(df) - 1]['TIME'], '%Y-%m')
#all_years = last_time.year - first_time.year


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
                

        
        
        
Cycle = Identify_Phase(4, OECD_CLI)
Cycle.keys()
Cycle['Expansion']






















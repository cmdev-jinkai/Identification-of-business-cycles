import pandas as pd
import numpy as np
import random

ALL_CLI = pd.read_csv('OECD.csv')
OECD_CLI = ALL_CLI[ALL_CLI.LOCATION == 'OECD'][['TIME', 'Value']]

SP_return = pd.read_csv('sp_price.csv')


len(OECD_CLI)
OECD_CLI.loc[ :,'Value']
OECD_CLI.iloc[1][0]

def Identify_Phase (Number_Phase, df):
    if Number_Phase == 2:
        phase1, phase2 = "Expension", "Recession"
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
        phase1, phase2, phase3, phase4 = "Expension", "Slowdown","Recession", "Recovery"
        month1, month2, month3, month4 = [], [], [], []
        
        
        
        
Cycle = Identify_Phase(2, OECD_CLI)


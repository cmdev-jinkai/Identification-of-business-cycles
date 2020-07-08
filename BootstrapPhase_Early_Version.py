# -*- coding: utf-8 -*-
"""
Name:Use Method of Bootstrap to predict the median term returns based on different phases
Author: Jinkai Zhang
Date: June 24, 2020

EXAMPLE AND RESULTS
Results: Mean of predicted return
Method: Bootstrap of bootstraps
Index: U.S S&P 500
Predicted years: 2 years (this allows users to choose the number of months)
Note: the prediction is based on the starting point at differnt phases

TWO PHASES IDENTIFICATION:
    Expansion: 4.41%
    Recession: 11.69%

FOUR PHASES IDENTIFICATION:
    Expansion: 3.07%
    Recession: 11.59%
    Slowdown: 6.84%
    Recovery: 11.25%

SIX PHASES IDENTIFICATION:
    Expansion: 4.21%
    Recession: 11.40%
    Slowdown: 3.09%
    Recovery: 11.06%
    DoubleUp: 6.6%
    DoubleDown: 10.8%

"""
import pandas as pd
import numpy as np
import random
from datetime import datetime
from IdentifyPhase_Early_Version import Identify_Phase
from Bootstrap import bootstrap

ALL_CLI = pd.read_csv('Data/OECD.csv')
OECD_CLI = ALL_CLI[ALL_CLI.LOCATION == 'OECD'][['TIME', 'Value']]
SP_return = pd.read_csv('Data/sp_price.csv')


def Format_Date (df):
    df.index = range(len(df))
    for i in range(len(df)):
        date = datetime.strptime(df.iloc[i]['Date'], '%m/%d/%Y')
        if date.month < 10:
            df.iloc[i, 0] = str(date.year) + '-0' + str(date.month)
        else:
            df.iloc[i, 0] = str(date.year) + '-' + str(date.month)
    return df

def Return_Collection (month_list, df, periods_month):
    Output_returns = []
    month_existence = df.iloc[:, 0].tolist()
    for i in range(len(month_list)):
        current_month = month_list[i]
        if current_month in month_existence:
            current_index = df[df.Date == current_month].index.tolist()[0]
            #print ([i, current_month])
            for j in range(1, periods_month + 1):
                if (current_index + j) < len(df):
                    Output_returns.append(df.iloc[current_index + j]['Return'])
    return Output_returns


def Bootstrap_Phase (cycle_indicator, df, periods_month, numbers_phase, phase_name, method = 'NED', condidence_interval = 80):
    if numbers_phase == 2:
        TwoPhases_Collection = Identify_Phase(2, cycle_indicator)
        if phase_name == 'Expansion':
            history_month = TwoPhases_Collection['Expansion']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        else: #phase_name == 'Recession':
            history_month = TwoPhases_Collection['Recession']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
    elif numbers_phase == 4:
        FourPhases_Collection = Identify_Phase(4, cycle_indicator)
        if phase_name == 'Expansion':
            history_month = FourPhases_Collection['Expansion']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'Recession':
            history_month = FourPhases_Collection['Recession']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'Slowdown':
            history_month = FourPhases_Collection['Slowdown']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'Recovery':
            history_month = FourPhases_Collection['Recovery']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
    elif numbers_phase == 6:
        SixPhases_Collection = Identify_Phase(6, cycle_indicator)
        if phase_name == 'Expansion':
            history_month = SixPhases_Collection['Expansion']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'Recession':
            history_month = SixPhases_Collection['Recession']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'Slowdown':
            history_month = SixPhases_Collection['Slowdown']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'Recovery':
            history_month = SixPhases_Collection['Recovery']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'DoubleUp':
            history_month = SixPhases_Collection['DoubleUp']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output
        elif phase_name == 'DoubleDown':
            history_month = SixPhases_Collection['DoubleDown']
            history_return = Return_Collection(history_month, df, periods_month)
            Output = bootstrap(history_return, periods_month, method, condidence_interval)
            return Output

if __name__ == '__main__':
    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ EXAMPLES ~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    SP_return = Format_Date (SP_return) #run this only onece
    #2 years prediction (24 months)  in 2-PHASE-identification
    Expansion_Twophases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 2, phase_name = 'Expansion')  
    print(Expansion_Twophases)
    Recession_Twophases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 2, phase_name = 'Recession')  
    print(Recession_Twophases)
    
    #2 years prediction (24 months)in 4-PASE-identification
    Expansion_Fourphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 4, phase_name = 'Expansion')  
    print(Expansion_Fourphases)
    Recession_Fourphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 4, phase_name = 'Recession')  
    print(Recession_Fourphases)
    Slowdown_Fourphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 4, phase_name = 'Slowdown')  
    print(Slowdown_Fourphases)
    Recovery_Fourphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 4, phase_name = 'Recovery')  
    print(Recovery_Fourphases)
    
    #2 years prediction (24 months)in 6-PASE-identification
    Expansion_Sixphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 6, phase_name = 'Expansion')  
    print(Expansion_Sixphases)
    Recession_Sixphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 6, phase_name = 'Recession')  
    print(Recession_Sixphases)
    Slowdown_Sixphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 6, phase_name = 'Slowdown')  
    print(Slowdown_Sixphases)
    Recovery_Sixphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 6, phase_name = 'Recovery')  
    print(Recovery_Sixphases)
    DoubleUp_Sixphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 6, phase_name = 'DoubleUp')  
    print(DoubleUp_Sixphases)
    DoubleDown_Sixphases = Bootstrap_Phase(OECD_CLI, SP_return, 24, numbers_phase = 6, phase_name = 'DoubleDown')  
    print(DoubleDown_Sixphases)
    
    
    
    
    
    
    
    
    
    

# -*- coding: utf-8 -*-
"""
Name:linkage between Bootstrap Method and Phase Identification Table
Author: Jinkai Zhang
Original Version: July 10, 2020
Revised Version: July 13, 2020

Early Ouputs (Annulized Return) using 2-years (24 months) prediction:
Data: S&P return data
    
Single Inputs (OECD only) (1964-2020):
        TWO PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 5.265, 'Standard Deviation(%)': 12.0993
            Recession: 'Mean(%)': 9.8065, 'Standard Deviation(%)': 9.5194

        FOUR PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 4.8671, 'Standard Deviation(%)': 9.4798
            Recession: 'Mean(%)': 9.4869, 'Standard Deviation(%)': 10.7159
            Slowdown: 'Mean(%)': 5.5946, 'Standard Deviation(%)': 13.8853
            Recovery: 'Mean(%)': 10.1108, 'Standard Deviation(%)': 8.2154

        SIX PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 3.9642, 'Standard Deviation(%)': 11.1693
            Recession: 'Mean(%)': 10.7005, 'Standard Deviation(%)': 10.7382
            Slowdown: 'Mean(%)': 7.7264, 'Standard Deviation(%)': 13.3532
            Recovery: 'Mean(%)': 7.502, 'Standard Deviation(%)': 6.9359
            Re_acceleration: 'Mean(%)': 1.7386, 'Standard Deviation(%)': 13.0856 (note: sample size 36)
            Double_dip: 'Mean(%)': 13.1571, 'Standard Deviation(%)': 5.63 (note: sample size 31)


Single Inputs (OECD only) (1993-2020):
        TWO PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 6.3539, 'Standard Deviation(%)': 12.7844
            Recession: 'Mean(%)': 11.286, 'Standard Deviation(%)': 12.4886

        FOUR PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 7.6372, 'Standard Deviation(%)': 9.8329
            Recession: 'Mean(%)': 8.7618, 'Standard Deviation(%)': 14.6362
            Slowdown: Mean(%)': 5.163, 'Standard Deviation(%)': 14.9105
            Recovery: 'Mean(%)': 13.5344, 'Standard Deviation(%)': 9.6558

        SIX PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 8.9226, 'Standard Deviation(%)': 9.7188
            Recession: 'Mean(%)': 11.8274, 'Standard Deviation(%)': 14.3121
            Slowdown: 'Mean(%)': 6.646, 'Standard Deviation(%)': 15.0044
            Recovery: 'Mean(%)': 10.7135, 'Standard Deviation(%)': 8.2993
            Re_acceleration: 'Mean(%)': -6.2503, 'Standard Deviation(%)': 13.1282 (note: sample size ONLY 19)
            Double_dip: 'Mean(%)': 11.9567, 'Standard Deviation(%)': 5.5312 (note: sample size ONLY 11)

    
    
    
        
Multiple Inputs (Composite Z-Score method) (1993-2020):
    
        Correlation Matrix of Z-Score
        Z1: Economic Growth - OECD CLI Index
        Z2: Consumer Sentiment - University of Michigan Consumer Sentiment Index 
        Z3: Financial Stress - Kansas City Financial Stress Index
        Z4: Unemployment Rate - U.S. unemployment rate;
        Z5: Producer Sentiment - ISM factor (ISM manufacturers’ survey production index);

              Z1        Z2        Z3        Z4        Z5
        Z1  1.000000  0.461546  0.375933  0.502463  0.677101
        Z2  0.461546  1.000000  0.265916  0.632296  0.473199
        Z3  0.375933  0.265916  1.000000  0.110936  0.458854
        Z4  0.502463  0.632296  0.110936  1.000000  0.187146
        Z5  0.677101  0.473199  0.458854  0.187146  1.000000
        
        
        TWO PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 9.3638, 'Standard Deviation(%)': 12.0728
            Recession: 'Mean(%)': 6.0512, 'Standard Deviation(%)': 14.2945

        FOUR PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 9.4059, 'Standard Deviation(%)': 11.6625
            Recession: 'Mean(%)': 3.0367, 'Standard Deviation(%)': 14.7808
            Slowdown: 'Mean(%)': 9.3756, 'Standard Deviation(%)': 12.5365
            Recovery: 'Mean(%)': 9.8559, 'Standard Deviation(%)': 12.6716

        SIX PHASES IDENTIFICATION:
            Expansion: 'Mean(%)': 7.1099, 'Standard Deviation(%)': 8.5921
            Recession: 'Mean(%)': -1.818, 'Standard Deviation(%)': 13.0884
            Slowdown: 'Mean(%)': 11.0346, 'Standard Deviation(%)': 14.0703
            Recovery: 'Mean(%)': 9.5122, 'Standard Deviation(%)': 8.7556
            Re_acceleration: 'Mean(%)': 10.0254, 'Standard Deviation(%)': 15.2299
            Double_dip: None (sample size less than 10)
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
from PHASES_in_Six_JR import get_cycle_phase
from Bootstrap import bootstrap

#add return columns to the phase df defined in IdentifyPhase_Scherer_Apel_2020.py
sp_return = pd.read_csv('Data/sp_price.csv')

LastDay_Leap = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
LastDay_NonLeap = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}


def Reform_SP500 (df):
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

sp_return = Reform_SP500(sp_return)


def Add_Return_Column(df_phase, df_return):
    df_phase.index = range(len(df_phase))
    df_return.index = range(len(df_return))
    date_begin = df_phase.iloc[0, 0]
    date_end = df_phase.iloc[len(df_phase) - 1, 0]
    index_begin = df_return[df_return.Date == date_begin].index.tolist()[0]
    index_end = df_return[df_return.Date == date_end].index.tolist()[0]
    Return = df_return.Index[index_begin : index_end + 1]
    Return.index = range(len(Return))
    df_phase['Return'] = Return
    return df_phase[['Date', 'phase', 'Return']]


#KEY FUNCTION
# df contains three columns named 'Date', 'phase', 'Return' (upper case for 'R')
# The Return is in the unit of % 
# phase_number: 2, 4, 6
# phase_name: input the estimated returns of which phase required
# periods_month is the horizon of prediction
# two method for choice: NED and FS
# TO BE EXTENDED to more phase names
# condidence_interval: defaul = 95
    
def Link_Phase_Bootstrap(df, phase_number, phase_name, periods_month, method = 'NED', condidence_interval = 95):
    df.index = range(len(df))
    
    def Return_Detection(df, begin_index, return_history, periods_month):
        begin_index += 1
        end_index = begin_index + periods_month
        if end_index - 1 <= len(df):
            returns_monthly = df.Return[begin_index:end_index].tolist()
            def plus_one (x): return (x/100 + 1)
            returns_monthly = list(map(plus_one, returns_monthly))
            #culmulate the monthly return to LTR
            returns_periods = np.prod(returns_monthly) - 1
            #Transfer from Cumulated return to Anualized return
            # (1 + Montly_Return) ^ periods_month - 1 = Cumul_Ret    ----(1)
            Montly_Return = (returns_periods + 1) ** (1 / periods_month) - 1
            # (1 + Montly_Return) ^ 12 - 1 = Anualized_Return    ----(2)
            Anualized_Return = (1 + Montly_Return) ** 12 - 1
            #transfer back to the unit of '%'
            Anualized_Return = Anualized_Return * 100
            return_history.append(Anualized_Return)
        else:
            pass
        return return_history
            
    if phase_number == 2:
        expansion = []
        contraction = []
        for i in range(len(df)):
            if df.phase[i] == 'expansion':
                expansion = Return_Detection(df, i, expansion, periods_month)
            elif df.phase[i] == 'contraction':
                contraction = Return_Detection(df, i, contraction, periods_month)
            else:
                print("Something goes wrong, please have a check")
        if phase_name == 'expansion':
            return bootstrap(expansion, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'contraction':
            return bootstrap(contraction, periods_month, method = method, condidence_interval = condidence_interval)
            print('please check the input of phase name')
            
    elif phase_number == 4:
        expansion = []
        contraction = []
        slowdown = []
        recovery = []
        for i in range(len(df)):
            if df.phase[i] == 'expansion':
                expansion = Return_Detection(df, i, expansion, periods_month)
            elif df.phase[i] == 'contraction':
                contraction = Return_Detection(df, i, contraction, periods_month)
            elif df.phase[i] == 'slowdown':
                slowdown = Return_Detection(df, i, slowdown, periods_month)
            elif df.phase[i] == 'recovery':
                recovery = Return_Detection(df, i, recovery, periods_month)
            else:
                print("Something goes wrong, please have a check")
        if phase_name == 'expansion':
            return bootstrap(expansion, periods_month, method = method , condidence_interval = condidence_interval)
        elif phase_name == 'contraction':
            return bootstrap(contraction, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'slowdown':
            return bootstrap(slowdown, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'recovery':
            return bootstrap(recovery, periods_month, method = method, condidence_interval = condidence_interval)
        else:
            print('please check the input of phase name')
    
    elif phase_number == 6:
        expansion = []
        contraction = []
        slowdown = []
        recovery = []
        double_dip = []
        re_acceleration = []
        for i in range(len(df)):
            if df.phase[i] == 'expansion':
                expansion = Return_Detection(df, i, expansion, periods_month)
            elif df.phase[i] == 'contraction':
                contraction = Return_Detection(df, i, contraction, periods_month)
            elif df.phase[i] == 'slowdown':
                slowdown = Return_Detection(df, i, slowdown, periods_month)
            elif df.phase[i] == 'recovery':
                recovery = Return_Detection(df, i, recovery, periods_month)
            elif df.phase[i] == 'double_dip':
                double_dip = Return_Detection(df, i, double_dip, periods_month)
            elif df.phase[i] == 're-acceleration':
                re_acceleration = Return_Detection(df, i, re_acceleration, periods_month)
            else:
                print("Something goes wrong, please have a check")
        if phase_name == 'expansion':
            return bootstrap(expansion, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'contraction':
            return bootstrap(contraction, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'slowdown':
            return bootstrap(slowdown, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'recovery':
            return bootstrap(recovery, periods_month, method = method, condidence_interval = condidence_interval)
        elif phase_name == 'double_dip':
            if len(double_dip) >= 10:
                print('There are ' + str(len(double_dip)) + ' historical cumulative returns for bootstrap in double_dip phase. Please check robustness manually.')
                return bootstrap(double_dip, periods_month, method = 'NED', condidence_interval = condidence_interval)
            else:
                print('There are no sufficient historical data of returns for phase of' + phase_name)
        elif phase_name == 're-acceleration':
            if len(re_acceleration) >= 10:
                print('There are ' + str(len(re_acceleration)) + ' historical cumulative returns for bootstrap in re_acceleration phase. Please check robustness manually.')
                return bootstrap(re_acceleration, periods_month, method = 'NED', condidence_interval = condidence_interval)
            else:
                print('There are no sufficient historical data of returns for phase of' + phase_name)
        else:
            print('please check the input of phase name')
    else:
        pass

if __name__ == '__main__':
    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ Inputs ~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    #please run all code in IdentifyPhase_Scherer_Apel_2020.py fist
    #input include thee columns which are 'Date', 'phase', 'Return'
    SingleInput_2Phases = Add_Return_Column(SingleInput_2Phases, sp_return)
    SingleInput_4Phases = Add_Return_Column(SingleInput_4Phases, sp_return)
    SingleInput_6Phases = Add_Return_Column(SingleInput_6Phases, sp_return)
    
    MultipleInput_2Phases = Add_Return_Column(MultipleInput_2Phases, sp_return)
    MultipleInput_4Phases = Add_Return_Column(MultipleInput_4Phases, sp_return)
    MultipleInput_6Phases = Add_Return_Column(MultipleInput_6Phases, sp_return)

    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ Outputs ~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    #annulized returns in prediction of 24 months returns
    
    Single_2Phase_Expansion = Link_Phase_Bootstrap(SingleInput_2Phases, 2, 'expansion', 24)
    print('Single_2Phase_Expansion')
    print(Single_2Phase_Expansion)
    Single_2Phase_contraction = Link_Phase_Bootstrap(SingleInput_2Phases, 2, 'contraction', 24)
    print('Single_2Phase_contraction')
    print(Single_2Phase_contraction)

    Single_4Phase_Expansion = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'expansion', 24)
    print('Single_4Phase_Expansion')
    print(Single_4Phase_Expansion)
    Single_4Phase_contraction = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'contraction', 24)
    print('Single_4Phase_contraction')
    print(Single_4Phase_contraction)
    Single_4Phase_Slowdown = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'slowdown', 24)
    print('Single_4Phase_Slowdown')
    print(Single_4Phase_Slowdown)
    Single_4Phase_Recovery = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'recovery', 24)
    print('Single_4Phase_Recovery')
    print(Single_4Phase_Recovery)
    
    Single_6Phase_Expansion = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'expansion', 24)
    print('Single_6Phase_Expansion')
    print(Single_6Phase_Expansion)
    Single_6Phase_contraction = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'contraction', 24)
    print('Single_6Phase_contraction')
    print(Single_6Phase_contraction)
    Single_6Phase_Slowdown = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'slowdown', 24)
    print('Single_6Phase_Slowdown')
    print(Single_6Phase_Slowdown)
    Single_6Phase_Recovery = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'recovery', 24)
    print('Single_6Phase_Recovery')
    print(Single_6Phase_Recovery)
    Single_6Phase_double_dip = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'double_dip', 24)
    print('Single_6Phase_double_dip')
    print(Single_6Phase_double_dip)
    Single_6Phase_re_acceleration = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 're-acceleration', 24)
    print('Single_6Phase_re_acceleration')
    print(Single_6Phase_re_acceleration)


    Multiple_2Phase_Expansion = Link_Phase_Bootstrap(MultipleInput_2Phases, 2, 'expansion', 24)
    print('Multiple_2Phase_Expansion')
    print(Multiple_2Phase_Expansion)
    Multiple_2Phase_contraction = Link_Phase_Bootstrap(MultipleInput_2Phases, 2, 'contraction', 24)
    print('Multiple_2Phase_contraction')
    print(Multiple_2Phase_contraction)

    Multiple_4Phase_Expansion = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'expansion', 24)
    print('Multiple_4Phase_Expansion')
    print(Multiple_4Phase_Expansion)
    Multiple_4Phase_contraction = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'contraction', 24)
    print('Multiple_4Phase_contraction')
    print(Multiple_4Phase_contraction)
    Multiple_4Phase_Slowdown = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'slowdown', 24)
    print('Multiple_4Phase_Slowdown')
    print(Multiple_4Phase_Slowdown)
    Multiple_4Phase_Recovery = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'recovery', 24)
    print('Multiple_4Phase_Recovery')
    print(Multiple_4Phase_Recovery)
    
    Multiple_6Phase_Expansion = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'expansion', 24)
    print('Multiple_6Phase_Expansion')
    print(Multiple_6Phase_Expansion)
    Multiple_6Phase_contraction = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'contraction', 24)
    print('Multiple_6Phase_contraction')
    print(Multiple_6Phase_contraction)
    Multiple_6Phase_Slowdown = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'slowdown', 24)
    print('Multiple_6Phase_Slowdown')
    print(Multiple_6Phase_Slowdown)
    Multiple_6Phase_Recovery = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'recovery', 24)
    print('Multiple_6Phase_Recovery')
    print(Multiple_6Phase_Recovery)
    Multiple_6Phase_double_dip = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'double_dip', 24)
    print('Multiple_6Phase_double_dip')
    print(Multiple_6Phase_double_dip)
    Multiple_6Phase_re_acceleration = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 're-acceleration', 24)
    print('Multiple_6Phase_re_acceleration')
    print(Multiple_6Phase_re_acceleration)








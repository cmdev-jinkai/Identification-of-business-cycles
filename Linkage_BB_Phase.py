# -*- coding: utf-8 -*-
"""
Name:linkage between Bootstrap Method and Phase Identification Table
Author: Jinkai Zhang
Date: July 10, 2020

Early Ouputs (Annulized Return) using 2-years (24 months) prediction:

Single Inputs (OECD only) (1964-2020):
        TWO PHASES IDENTIFICATION:
            Expansion: 5.55%
            Recession: 10.35%

        FOUR PHASES IDENTIFICATION:
            Expansion: 4.64%
            Recession: 9.60%
            Slowdown: 5.48%
            Recovery: 9.62%

        SIX PHASES IDENTIFICATION:
            Expansion: 3.82%
            Recession: 10.93%
            Slowdown: 7.42%
            Recovery: 7.44%
            Re_acceleration: 1.34%
            Double_dip: 13.50%
    
Multiple Inputs (Composite Z-Score method) (1993-2020):
        TWO PHASES IDENTIFICATION:
            Expansion: 9.14%
            Recession: 6.09%

        FOUR PHASES IDENTIFICATION:
            Expansion: 9.20%
            Recession: 2.99%
            Slowdown: 8.72%
            Recovery: 9.91%

        SIX PHASES IDENTIFICATION:
            Expansion: 7.04%
            Recession: -0.88%
            Slowdown: 10.32%
            Recovery: 9.36%
            Re_acceleration: 9.53%
            Double_dip: 17.68%
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




def Link_Phase_Bootstrap(df, phase_number, phase_name, periods_month):
    df.index = range(len(df))
    
    def Return_Detection(df, current_index, return_history, periods_month):
        current_index += 1
        curent_loop = 1
        while current_index < len(df) and curent_loop <= periods_month:
            return_history.append(df.Return[current_index])
            curent_loop += 1
            current_index += 1
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
            return bootstrap(expansion, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'contraction':
            return bootstrap(contraction, periods_month, method = 'NED', condidence_interval = 80)
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
            return bootstrap(expansion, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'contraction':
            return bootstrap(contraction, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'slowdown':
            return bootstrap(slowdown, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'recovery':
            return bootstrap(recovery, periods_month, method = 'NED', condidence_interval = 80)
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
            return bootstrap(expansion, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'contraction':
            return bootstrap(contraction, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'slowdown':
            return bootstrap(slowdown, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'recovery':
            return bootstrap(recovery, periods_month, method = 'NED', condidence_interval = 80)
        elif phase_name == 'double_dip':
            if len(double_dip) >= 50:
                return bootstrap(double_dip, periods_month, method = 'NED', condidence_interval = 80)
            else:
                print('There are no sufficient historical data of returns for phase of' + phase_name)
        elif phase_name == 're-acceleration':
            if len(double_dip) >= 50:
                return bootstrap(re_acceleration, periods_month, method = 'NED', condidence_interval = 80)
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









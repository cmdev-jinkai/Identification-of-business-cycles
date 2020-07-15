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
            Expansion: {'Mean(%)': 5.5418, 'Standard Deviation(%)': 12.5478, 'Median(%)': 5.5426, '25th(%)': -2.9203, '75th(%)': 14.0062, 'Confidence Interval(95)(%)': [-15.0993, 26.1787]}
            Recession: {'Mean(%)': 9.255, 'Standard Deviation(%)': 9.2269, 'Median(%)': 9.2553, '25th(%)': 3.0327, '75th(%)': 15.478, 'Confidence Interval(95)(%)': [-5.9236, 24.431]}

        FOUR PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 6.0173, 'Standard Deviation(%)': 10.8531, 'Median(%)': 6.0173, '25th(%)': -1.3034, '75th(%)': 13.337, 'Confidence Interval(95)(%)': [-11.8328, 23.8667]}
            Recession: {'Mean(%)': 9.1006, 'Standard Deviation(%)': 10.5081, 'Median(%)': 9.1003, '25th(%)': 2.014, '75th(%)': 16.1888, 'Confidence Interval(95)(%)': [-8.1839, 26.3848]}
            Slowdown:  {'Mean(%)': 5.0705, 'Standard Deviation(%)': 14.0915, 'Median(%)': 5.0689, '25th(%)': -4.4352, '75th(%)': 14.5747, 'Confidence Interval(95)(%)': [-18.106, 28.2479]}
            Recovery:  {'Mean(%)': 9.4332, 'Standard Deviation(%)': 7.4936, 'Median(%)': 9.4329, '25th(%)': 4.3783, '75th(%)': 14.4879, 'Confidence Interval(95)(%)': [-2.8906, 21.7583]}

        SIX PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 5.2696, 'Standard Deviation(%)': 11.8592, 'Median(%)': 5.2715, '25th(%)': -2.7303, '75th(%)': 13.2697, 'Confidence Interval(95)(%)': [-14.2395, 24.7728]}
            Recession: {'Mean(%)': 10.021, 'Standard Deviation(%)': 10.2269, 'Median(%)': 10.0215, '25th(%)': 3.1238, '75th(%)': 16.9195, 'Confidence Interval(95)(%)': [-6.8003, 26.8425]}
            Slowdown: {'Mean(%)': 7.1837, 'Standard Deviation(%)': 13.4067, 'Median(%)': 7.1831, '25th(%)': -1.8573, '75th(%)': 16.2274, 'Confidence Interval(95)(%)': [-14.8669, 29.2369]}
            Recovery: {'Mean(%)': 7.6315, 'Standard Deviation(%)': 7.0785, 'Median(%)': 7.6319, '25th(%)': 2.8565, '75th(%)': 12.4059, 'Confidence Interval(95)(%)': [-4.012, 19.275]}
            Re_acceleration: {'Mean(%)': 1.2145, 'Standard Deviation(%)': 13.882, 'Median(%)': 1.215, '25th(%)': -8.1476, '75th(%)': 10.5775, 'Confidence Interval(95)(%)': [-21.6204, 24.0479]} 
                                    (note: sample size 32)
            Double_dip: {'Mean(%)': 12.8741, 'Standard Deviation(%)': 5.7374, 'Median(%)': 12.8741, '25th(%)': 9.004, '75th(%)': 16.7444, 'Confidence Interval(95)(%)': [3.4378, 22.3116]}
                                    (note: sample size 26)


Single Inputs (OECD only) (1993-2020):
        TWO PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 2.6818, 'Standard Deviation(%)': 13.1142, 'Median(%)': 2.6815, '25th(%)': -6.1635, '75th(%)': 11.5278, 'Confidence Interval(95)(%)': [-18.8905, 24.2501]}
            Recession: {'Mean(%)': 10.1284, 'Standard Deviation(%)': 11.7021, 'Median(%)': 10.1287, '25th(%)': 2.2367, '75th(%)': 18.0215, 'Confidence Interval(95)(%)': [-9.1202, 29.3771]}

        FOUR PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 9.2586, 'Standard Deviation(%)': 11.2192, 'Median(%)': 9.2575, '25th(%)': 1.6919, '75th(%)': 16.8279, 'Confidence Interval(95)(%)': [-9.1935, 27.7113]}
            Recession: {'Mean(%)': 8.2052, 'Standard Deviation(%)': 13.1667, 'Median(%)': 8.2043, '25th(%)': -0.6754, '75th(%)': 17.0859, 'Confidence Interval(95)(%)': [-13.4525, 29.8643]}
            Slowdown: {'Mean(%)': 4.5107, 'Standard Deviation(%)': 15.4757, 'Median(%)': 4.5101, '25th(%)': -5.9304, '75th(%)': 14.9485, 'Confidence Interval(95)(%)': [-20.9432, 29.9723]}
            Recovery: {'Mean(%)': 12.4265, 'Standard Deviation(%)': 9.1518, 'Median(%)': 12.4267, '25th(%)': 6.2535, '75th(%)': 18.5992, 'Confidence Interval(95)(%)': [-2.6279, 27.4786]}

        SIX PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 10.1806, 'Standard Deviation(%)': 10.3191, 'Median(%)': 10.1796, '25th(%)': 3.2202, '75th(%)': 17.142, 'Confidence Interval(95)(%)': [-6.7933, 27.1546]}
            Recession: {'Mean(%)': 10.1718, 'Standard Deviation(%)': 13.0645, 'Median(%)': 10.1707, '25th(%)': 1.3598, '75th(%)': 18.9859, 'Confidence Interval(95)(%)': [-11.319, 31.6572]}
            Slowdown: {'Mean(%)': 6.5957, 'Standard Deviation(%)': 15.5456, 'Median(%)': 6.5978, '25th(%)': -3.8907, '75th(%)': 17.0803, 'Confidence Interval(95)(%)': [-18.9735, 32.1632]}
            Recovery: {'Mean(%)': 10.6466, 'Standard Deviation(%)': 8.7354, 'Median(%)': 10.6472, '25th(%)': 4.7549, '75th(%)': 16.5379, 'Confidence Interval(95)(%)': [-3.7199, 25.0161]}
            Re_acceleration: {'Mean(%)': -7.335, 'Standard Deviation(%)': 12.6306, 'Median(%)': -7.3352, '25th(%)': -15.8535, '75th(%)': 1.185, 'Confidence Interval(95)(%)': [-28.1084, 13.4384]}
                    (note: sample size ONLY 18)
            Double_dip: {'Mean(%)': 11.3828, 'Standard Deviation(%)': 5.3678, 'Median(%)': 11.3833, '25th(%)': 7.7622, '75th(%)': 15.0031, 'Confidence Interval(95)(%)': [2.5544, 20.2126]}
                    (note: sample size ONLY 12)

    
    
    
        
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
            Expansion: {'Mean(%)': 9.2196, 'Standard Deviation(%)': 12.1711, 'Median(%)': 9.2206, '25th(%)': 1.0096, '75th(%)': 17.4295, 'Confidence Interval(95)(%)': [-10.8002, 29.2346]}
            Recession: {'Mean(%)': 6.6456, 'Standard Deviation(%)': 14.0232, 'Median(%)': 6.6455, '25th(%)': -2.8125, '75th(%)': 16.1024, 'Confidence Interval(95)(%)': [-16.4187, 29.714]}

        FOUR PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 8.7557, 'Standard Deviation(%)': 11.8746, 'Median(%)': 8.7551, '25th(%)': 0.7463, '75th(%)': 16.7635, 'Confidence Interval(95)(%)': [-10.7764, 28.2873]}
            Recession: {'Mean(%)': 3.398, 'Standard Deviation(%)': 14.4936, 'Median(%)': 3.4003, '25th(%)': -6.379, '75th(%)': 13.1752, 'Confidence Interval(95)(%)': [-20.4421, 27.236]}
            Slowdown: {'Mean(%)': 9.8489, 'Standard Deviation(%)': 12.5483, 'Median(%)': 9.8488, '25th(%)': 1.3842, '75th(%)': 18.3128, 'Confidence Interval(95)(%)': [-10.7924, 30.4881]}
            Recovery: {'Mean(%)': 10.5003, 'Standard Deviation(%)': 12.3862, 'Median(%)': 10.5014, '25th(%)': 2.1457, '75th(%)': 18.8545, 'Confidence Interval(95)(%)': [-9.8738, 30.8751]}

        SIX PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 11.2394, 'Standard Deviation(%)': 10.6285, 'Median(%)': 11.2393, '25th(%)': 4.0696, '75th(%)': 18.4078, 'Confidence Interval(95)(%)': [-6.2417, 28.7227]}
            Recession: {'Mean(%)': 1.4846, 'Standard Deviation(%)': 15.3556, 'Median(%)': 1.4848, '25th(%)': -8.8729, '75th(%)': 11.844, 'Confidence Interval(95)(%)': [-23.7735, 26.7413]}
            Slowdown: {'Mean(%)': 9.8121, 'Standard Deviation(%)': 13.8501, 'Median(%)': 9.813, '25th(%)': 0.47, '75th(%)': 19.1534, 'Confidence Interval(95)(%)': [-12.9697, 32.5937]}
            Recovery: {'Mean(%)': 10.9936, 'Standard Deviation(%)': 9.2984, 'Median(%)': 10.9941, '25th(%)': 4.7208, '75th(%)': 17.2638, 'Confidence Interval(95)(%)': [-4.3004, 26.2871]}
            Re_acceleration: {'Mean(%)': 2.6818, 'Standard Deviation(%)': 13.1142, 'Median(%)': 2.6815, '25th(%)': -6.1635, '75th(%)': 11.5278, 'Confidence Interval(95)(%)': [-18.8905, 24.2501]}
                            (note: sample size 37)
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








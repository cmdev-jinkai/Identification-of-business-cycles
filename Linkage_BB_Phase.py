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
            Expansion: {'Mean(%)': 5.5872, 'Standard Deviation(%)': 12.5553, 'Median(%)': 5.588, '25th(%)': -2.8806, '75th(%)': 14.0565, 'Confidence Interval(95)(%)': [-15.067, 26.2353]}
            Recession: {'Mean(%)': 9.2208, 'Standard Deviation(%)': 9.2198, 'Median(%)': 9.2202, '25th(%)': 3.0021, '75th(%)': 15.4392, 'Confidence Interval(95)(%)': [-5.9448, 24.3846]}

        FOUR PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 5.7928, 'Standard Deviation(%)': 10.7167, 'Median(%)': 5.7919, '25th(%)': -1.4356, '75th(%)': 13.0203, 'Confidence Interval(95)(%)': [-11.8335, 23.4214]}
            Recession: {'Mean(%)': 8.8764, 'Standard Deviation(%)': 10.431, 'Median(%)': 8.878, '25th(%)': 1.8408, '75th(%)': 15.9121, 'Confidence Interval(95)(%)': [-8.2812, 26.031]}
            Slowdown:  {'Mean(%)': 5.7508, 'Standard Deviation(%)': 14.2567, 'Median(%)': 5.7505, '25th(%)': -3.865, '75th(%)': 15.3649, 'Confidence Interval(95)(%)': [-17.6977, 29.2003]}
            Recovery:  {'Mean(%)': 9.2871, 'Standard Deviation(%)': 7.3566, 'Median(%)': 9.2873, '25th(%)': 4.325, '75th(%)': 14.2495, 'Confidence Interval(95)(%)': [-2.8132, 21.3882]}

        SIX PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 5.2695, 'Standard Deviation(%)': 11.8587, 'Median(%)': 5.2701, '25th(%)': -2.7288, '75th(%)': 13.2676, 'Confidence Interval(95)(%)': [-14.2379, 24.7729]}
            Recession: {'Mean(%)': 10.0212, 'Standard Deviation(%)': 10.2286, 'Median(%)': 10.0228, '25th(%)': 3.1215, '75th(%)': 16.9221, 'Confidence Interval(95)(%)': [-6.8024, 26.841]}
            Slowdown: {'Mean(%)': 7.1842, 'Standard Deviation(%)': 13.4072, 'Median(%)': 7.1839, '25th(%)': -1.8577, '75th(%)': 16.2262, 'Confidence Interval(95)(%)': [-14.867, 29.2377]}
            Recovery: {'Mean(%)': 7.6323, 'Standard Deviation(%)': 7.0786, 'Median(%)': 7.633, '25th(%)': 2.8572, '75th(%)': 12.4071, 'Confidence Interval(95)(%)': [-4.0113, 19.2743]}
            Re_acceleration: {'Mean(%)': 1.2167, 'Standard Deviation(%)': 13.8811, 'Median(%)': 1.2154, '25th(%)': -8.1452, '75th(%)': 10.5797, 'Confidence Interval(95)(%)': [-21.613, 24.0514]}
                                    (note: sample size 32)
            Double_dip: {'Mean(%)': 12.8732, 'Standard Deviation(%)': 5.7374, 'Median(%)': 12.8744, '25th(%)': 9.0033, '75th(%)': 16.7435, 'Confidence Interval(95)(%)': [3.4357, 22.3099]}
                                    (note: sample size 26)


Single Inputs (OECD only) (1993-2020):
        TWO PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 7.1355, 'Standard Deviation(%)': 13.5051, 'Median(%)': 7.1353, '25th(%)': -1.9728, '75th(%)': 16.2432, 'Confidence Interval(95)(%)': [-15.0768, 29.3492]}
            Recession: {'Mean(%)': 10.1279, 'Standard Deviation(%)': 11.7038, 'Median(%)': 10.1279, '25th(%)': 2.2325, '75th(%)': 18.0222, 'Confidence Interval(95)(%)': [-9.1208, 29.3806]}

        FOUR PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 9.0855, 'Standard Deviation(%)': 11.1413, 'Median(%)': 9.0854, '25th(%)': 1.5711, '75th(%)': 16.6007, 'Confidence Interval(95)(%)': [-9.2391, 27.4127]}
            Recession: {'Mean(%)': 7.8286, 'Standard Deviation(%)': 13.1321, 'Median(%)': 7.8286, '25th(%)': -1.0292, '75th(%)': 16.6844, 'Confidence Interval(95)(%)': [-13.7699, 29.4299]}
            Slowdown: {'Mean(%)': 5.5169, 'Standard Deviation(%)': 15.675, 'Median(%)': 5.5169, '25th(%)': -5.0563, '75th(%)': 16.0895, 'Confidence Interval(95)(%)': [-20.2639, 31.3]}
            Recovery: {'Mean(%)': 12.0977, 'Standard Deviation(%)': 8.99, 'Median(%)': 12.0975, '25th(%)': 6.0332, '75th(%)': 18.1624, 'Confidence Interval(95)(%)': [-2.6893, 26.8847]}

        SIX PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 10.1823, 'Standard Deviation(%)': 10.3195, 'Median(%)': 10.1808, '25th(%)': 3.2234, '75th(%)': 17.1423, 'Confidence Interval(95)(%)': [-6.7904, 27.1552]}
            Recession: {'Mean(%)': 10.17, 'Standard Deviation(%)': 13.0633, 'Median(%)': 10.1698, '25th(%)': 1.359, '75th(%)': 18.9822, 'Confidence Interval(95)(%)': [-11.3176, 31.6544]}
            Slowdown: {'Mean(%)': 6.5948, 'Standard Deviation(%)': 15.5462, 'Median(%)': 6.5947, '25th(%)': -3.89, '75th(%)': 17.0805, 'Confidence Interval(95)(%)': [-18.9745, 32.1671]}
            Recovery: {'Mean(%)': 10.647, 'Standard Deviation(%)': 8.7357, 'Median(%)': 10.6475, '25th(%)': 4.7551, '75th(%)': 16.5386, 'Confidence Interval(95)(%)': [-3.7218, 25.0146]}
            Re_acceleration: {'Mean(%)': -7.3354, 'Standard Deviation(%)': 12.631, 'Median(%)': -7.3361, '25th(%)': -15.8542, '75th(%)': 1.1819, 'Confidence Interval(95)(%)': [-28.1097, 13.4403]}
                    (note: sample size ONLY 18)
            Double_dip: {'Mean(%)': 11.3835, 'Standard Deviation(%)': 5.3678, 'Median(%)': 11.3827, '25th(%)': 7.7626, '75th(%)': 15.0043, 'Confidence Interval(95)(%)': [2.5558, 20.2128]}
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
            Expansion: {'Mean(%)': 9.0786, 'Standard Deviation(%)': 12.3315, 'Median(%)': 9.0785, '25th(%)': 0.7596, '75th(%)': 17.3967, 'Confidence Interval(95)(%)': [-11.2044, 29.3621]}
            Recession: {'Mean(%)': 6.8877, 'Standard Deviation(%)': 13.8105, 'Median(%)': 6.8883, '25th(%)': -2.4266, '75th(%)': 16.2019, 'Confidence Interval(95)(%)': [-15.8292, 29.6042]}

        FOUR PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 8.9271, 'Standard Deviation(%)': 13.0207, 'Median(%)': 8.9277, '25th(%)': 0.1439, '75th(%)': 17.7102, 'Confidence Interval(95)(%)': [-12.4892, 30.3421]}
            Recession: {'Mean(%)': 3.4395, 'Standard Deviation(%)': 14.8016, 'Median(%)': 3.4416, '25th(%)': -6.5467, '75th(%)': 13.4246, 'Confidence Interval(95)(%)': [-20.9044, 27.7841]}
            Slowdown: {'Mean(%)': 9.3173, 'Standard Deviation(%)': 11.5359, 'Median(%)': 9.3172, '25th(%)': 1.5363, '75th(%)': 17.0988, 'Confidence Interval(95)(%)': [-9.6577, 28.2903]}
            Recovery: {'Mean(%)': 11.5569, 'Standard Deviation(%)': 10.4311, 'Median(%)': 11.5575, '25th(%)': 4.5226, '75th(%)': 18.5923, 'Confidence Interval(95)(%)': [-5.5989, 28.7139]}

        SIX PHASES IDENTIFICATION:
            Expansion: {'Mean(%)': 11.2373, 'Standard Deviation(%)': 10.6271, 'Median(%)': 11.2342, '25th(%)': 4.0699, '75th(%)': 18.4056, 'Confidence Interval(95)(%)': [-6.2382, 28.7177]}
            Recession: {'Mean(%)': 1.4836, 'Standard Deviation(%)': 15.3541, 'Median(%)': 1.4851, '25th(%)': -8.8732, '75th(%)': 11.8401, 'Confidence Interval(95)(%)': [-23.7689, 26.7367]}
            Slowdown: {'Mean(%)': 10.1912, 'Standard Deviation(%)': 13.4637, 'Median(%)': 10.1906, '25th(%)': 1.1088, '75th(%)': 19.2718, 'Confidence Interval(95)(%)': [-11.95, 32.337]}
            Recovery: {'Mean(%)': 10.995, 'Standard Deviation(%)': 9.3002, 'Median(%)': 10.9963, '25th(%)': 4.7219, '75th(%)': 17.2673, 'Confidence Interval(95)(%)': [-4.3038, 26.2911]}
            Re_acceleration: {'Mean(%)': 1.9974, 'Standard Deviation(%)': 13.5896, 'Median(%)': 1.997, '25th(%)': -7.1696, '75th(%)': 11.163, 'Confidence Interval(95)(%)': [-20.3516, 24.3518]}{'Mean(%)': 2.6818, 'Standard Deviation(%)': 13.1142, 'Median(%)': 2.6815, '25th(%)': -6.1635, '75th(%)': 11.5278, 'Confidence Interval(95)(%)': [-18.8905, 24.2501]}
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
    
# def Link_Phase_Bootstrap(df, phase_number, phase_name, periods_month, method = 'NED', condidence_interval = 95):
#     df.index = range(len(df))
    
#     def Return_Detection(df, begin_index, return_history, periods_month):
#         begin_index += 1
#         end_index = begin_index + periods_month
#         if end_index - 1 <= len(df):
#             returns_monthly = df.Return[begin_index:end_index].tolist()
#             def plus_one (x): return (x/100 + 1)
#             returns_monthly = list(map(plus_one, returns_monthly))
#             #culmulate the monthly return to LTR
#             returns_periods = np.prod(returns_monthly) - 1
#             #Transfer from Cumulated return to Anualized return
#             # (1 + Montly_Return) ^ periods_month - 1 = Cumul_Ret    ----(1)
#             Montly_Return = (returns_periods + 1) ** (1 / periods_month) - 1
#             # (1 + Montly_Return) ^ 12 - 1 = Anualized_Return    ----(2)
#             Anualized_Return = (1 + Montly_Return) ** 12 - 1
#             #transfer back to the unit of '%'
#             Anualized_Return = Anualized_Return * 100
#             return_history.append(Anualized_Return)
#         else:
#             pass
#         return return_history
            
#     if phase_number == 2:
#         expansion = []
#         contraction = []
#         for i in range(len(df)):
#             if df.phase[i] == 'expansion':
#                 expansion = Return_Detection(df, i, expansion, periods_month)
#             elif df.phase[i] == 'contraction':
#                 contraction = Return_Detection(df, i, contraction, periods_month)
#             else:
#                 print("Something goes wrong, please have a check")
#         if phase_name == 'expansion':
#             return bootstrap(expansion, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'contraction':
#             return bootstrap(contraction, periods_month, method = method, condidence_interval = condidence_interval)
#             print('please check the input of phase name')
            
#     elif phase_number == 4:
#         expansion = []
#         contraction = []
#         slowdown = []
#         recovery = []
#         for i in range(len(df)):
#             if df.phase[i] == 'expansion':
#                 expansion = Return_Detection(df, i, expansion, periods_month)
#             elif df.phase[i] == 'contraction':
#                 contraction = Return_Detection(df, i, contraction, periods_month)
#             elif df.phase[i] == 'slowdown':
#                 slowdown = Return_Detection(df, i, slowdown, periods_month)
#             elif df.phase[i] == 'recovery':
#                 recovery = Return_Detection(df, i, recovery, periods_month)
#             else:
#                 print("Something goes wrong, please have a check")
#         if phase_name == 'expansion':
#             return bootstrap(expansion, periods_month, method = method , condidence_interval = condidence_interval)
#         elif phase_name == 'contraction':
#             return bootstrap(contraction, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'slowdown':
#             return bootstrap(slowdown, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'recovery':
#             return bootstrap(recovery, periods_month, method = method, condidence_interval = condidence_interval)
#         else:
#             print('please check the input of phase name')
    
#     elif phase_number == 6:
#         expansion = []
#         contraction = []
#         slowdown = []
#         recovery = []
#         double_dip = []
#         re_acceleration = []
#         for i in range(len(df)):
#             if df.phase[i] == 'expansion':
#                 expansion = Return_Detection(df, i, expansion, periods_month)
#             elif df.phase[i] == 'contraction':
#                 contraction = Return_Detection(df, i, contraction, periods_month)
#             elif df.phase[i] == 'slowdown':
#                 slowdown = Return_Detection(df, i, slowdown, periods_month)
#             elif df.phase[i] == 'recovery':
#                 recovery = Return_Detection(df, i, recovery, periods_month)
#             elif df.phase[i] == 'double_dip':
#                 double_dip = Return_Detection(df, i, double_dip, periods_month)
#             elif df.phase[i] == 're-acceleration':
#                 re_acceleration = Return_Detection(df, i, re_acceleration, periods_month)
#             else:
#                 print("Something goes wrong, please have a check")
#         if phase_name == 'expansion':
#             return bootstrap(expansion, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'contraction':
#             return bootstrap(contraction, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'slowdown':
#             return bootstrap(slowdown, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'recovery':
#             return bootstrap(recovery, periods_month, method = method, condidence_interval = condidence_interval)
#         elif phase_name == 'double_dip':
#             if len(double_dip) >= 10:
#                 print('There are ' + str(len(double_dip)) + ' historical cumulative returns for bootstrap in double_dip phase. Please check robustness manually.')
#                 return bootstrap(double_dip, periods_month, method = 'NED', condidence_interval = condidence_interval)
#             else:
#                 print('There are no sufficient historical data of returns for phase of' + phase_name)
#         elif phase_name == 're-acceleration':
#             if len(re_acceleration) >= 10:
#                 print('There are ' + str(len(re_acceleration)) + ' historical cumulative returns for bootstrap in re_acceleration phase. Please check robustness manually.')
#                 return bootstrap(re_acceleration, periods_month, method = 'NED', condidence_interval = condidence_interval)
#             else:
#                 print('There are no sufficient historical data of returns for phase of' + phase_name)
#         else:
#             print('please check the input of phase name')
#     else:
#         pass

def Link_Phase_Bootstrap(df, periods_month, method = 'NED', condidence_interval = 95):
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
    
    list_phases = list(df['phase'].drop_duplicates())
    output = dict()
    return_phases = dict()
    for i in range(len(list_phases)):
        return_phases[list_phases[i]] = []
        
    for i in range(len(df)):
        return_phases[df.phase[i]] = Return_Detection(df, i, return_phases[df.phase[i]], periods_month)

    for i in range(len(list_phases)):
        if len(return_phases[list_phases[i]]) >= 30:
            output[list_phases[i]] = bootstrap(return_phases[list_phases[i]], periods_month, method = method, condidence_interval = condidence_interval)
        elif len(return_phases[list_phases[i]]) < 30 and len(return_phases[list_phases[i]]) >= 5:
            print('Warning: There are ' + str(len(return_phases[list_phases[i]])) + ' historical cumulative returns for bootstrap in phase of ' + list_phases[i] + '. Please check the robustness manually.')
            output[list_phases[i]] = bootstrap(return_phases[list_phases[i]], periods_month, method = method, condidence_interval = condidence_interval)
        else:
            output[list_phases[i]] = dict()
            print('There are no sufficient historical data of returns for phase of ' + list_phases[i])
        
    return output

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
    
    # Single_2Phase_Expansion = Link_Phase_Bootstrap(SingleInput_2Phases, 2, 'expansion', 24)
    # print('Single_2Phase_Expansion')
    # print(Single_2Phase_Expansion)
    # Single_2Phase_contraction = Link_Phase_Bootstrap(SingleInput_2Phases, 2, 'contraction', 24)
    # print('Single_2Phase_contraction')
    # print(Single_2Phase_contraction)

    # Single_4Phase_Expansion = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'expansion', 24)
    # print('Single_4Phase_Expansion')
    # print(Single_4Phase_Expansion)
    # Single_4Phase_contraction = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'contraction', 24)
    # print('Single_4Phase_contraction')
    # print(Single_4Phase_contraction)
    # Single_4Phase_Slowdown = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'slowdown', 24)
    # print('Single_4Phase_Slowdown')
    # print(Single_4Phase_Slowdown)
    # Single_4Phase_Recovery = Link_Phase_Bootstrap(SingleInput_4Phases, 4, 'recovery', 24)
    # print('Single_4Phase_Recovery')
    # print(Single_4Phase_Recovery)
    
    # Single_6Phase_Expansion = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'expansion', 24)
    # print('Single_6Phase_Expansion')
    # print(Single_6Phase_Expansion)
    # Single_6Phase_contraction = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'contraction', 24)
    # print('Single_6Phase_contraction')
    # print(Single_6Phase_contraction)
    # Single_6Phase_Slowdown = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'slowdown', 24)
    # print('Single_6Phase_Slowdown')
    # print(Single_6Phase_Slowdown)
    # Single_6Phase_Recovery = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'recovery', 24)
    # print('Single_6Phase_Recovery')
    # print(Single_6Phase_Recovery)
    # Single_6Phase_double_dip = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 'double_dip', 24)
    # print('Single_6Phase_double_dip')
    # print(Single_6Phase_double_dip)
    # Single_6Phase_re_acceleration = Link_Phase_Bootstrap(SingleInput_6Phases, 6, 're-acceleration', 24)
    # print('Single_6Phase_re_acceleration')
    # print(Single_6Phase_re_acceleration)


    # Multiple_2Phase_Expansion = Link_Phase_Bootstrap(MultipleInput_2Phases, 2, 'expansion', 24)
    # print('Multiple_2Phase_Expansion')
    # print(Multiple_2Phase_Expansion)
    # Multiple_2Phase_contraction = Link_Phase_Bootstrap(MultipleInput_2Phases, 2, 'contraction', 24)
    # print('Multiple_2Phase_contraction')
    # print(Multiple_2Phase_contraction)

    # Multiple_4Phase_Expansion = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'expansion', 24)
    # print('Multiple_4Phase_Expansion')
    # print(Multiple_4Phase_Expansion)
    # Multiple_4Phase_contraction = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'contraction', 24)
    # print('Multiple_4Phase_contraction')
    # print(Multiple_4Phase_contraction)
    # Multiple_4Phase_Slowdown = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'slowdown', 24)
    # print('Multiple_4Phase_Slowdown')
    # print(Multiple_4Phase_Slowdown)
    # Multiple_4Phase_Recovery = Link_Phase_Bootstrap(MultipleInput_4Phases, 4, 'recovery', 24)
    # print('Multiple_4Phase_Recovery')
    # print(Multiple_4Phase_Recovery)
    
    # Multiple_6Phase_Expansion = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'expansion', 24)
    # print('Multiple_6Phase_Expansion')
    # print(Multiple_6Phase_Expansion)
    # Multiple_6Phase_contraction = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'contraction', 24)
    # print('Multiple_6Phase_contraction')
    # print(Multiple_6Phase_contraction)
    # Multiple_6Phase_Slowdown = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'slowdown', 24)
    # print('Multiple_6Phase_Slowdown')
    # print(Multiple_6Phase_Slowdown)
    # Multiple_6Phase_Recovery = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'recovery', 24)
    # print('Multiple_6Phase_Recovery')
    # print(Multiple_6Phase_Recovery)
    # Multiple_6Phase_double_dip = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 'double_dip', 24)
    # print('Multiple_6Phase_double_dip')
    # print(Multiple_6Phase_double_dip)
    # Multiple_6Phase_re_acceleration = Link_Phase_Bootstrap(MultipleInput_6Phases, 6, 're-acceleration', 24)
    # print('Multiple_6Phase_re_acceleration')
    # print(Multiple_6Phase_re_acceleration)


    Single_2Phase = Link_Phase_Bootstrap(SingleInput_2Phases, 24)
    Single_4Phase = Link_Phase_Bootstrap(SingleInput_4Phases, 24)
    Single_6Phase = Link_Phase_Bootstrap(SingleInput_6Phases, 24)

    Multiple_2Phase = Link_Phase_Bootstrap(MultipleInput_2Phases, 24)
    Multiple_4Phase = Link_Phase_Bootstrap(MultipleInput_4Phases, 24)
    Multiple_6Phase = Link_Phase_Bootstrap(MultipleInput_6Phases, 24)




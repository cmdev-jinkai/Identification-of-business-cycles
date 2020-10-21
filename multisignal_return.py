# -*- coding: utf-8 -*-
"""
Name: Results estimates across different years's horizons for 30 countries
Author: Jinkai Zhang
Date: October 13, 2020

"""
import pickle
import pandas as pd
import numpy as np
import random
from datetime import datetime
from PHASES_in_Six_JR import get_cycle_phase
from Bootstrap import bootstrap
from Linkage_BB_Phase import Link_Phase_Bootstrap
from collections import Counter


root = "Jinkai_data.pickle"
    
with open(root, 'rb') as f:
    data = pickle.load(f)
    
root2 = "Investable_data_update.pickle"
    
with open(root2, 'rb') as f:
    data_return = pickle.load(f)

data.keys()
data_return['Philippines']

def Get_Zscore (df, rolling_year = 3):
    df = df.dropna()
    # df['Date'] = df.index
    df.columns = ['Index']
    rolling_month = rolling_year * 12
    zscore = [np.nan for i in range(rolling_month - 1)]
    for i in range(rolling_month - 1, len(df)):
        start_index = i - rolling_month + 1
        end_index = i
        series = df['Index'][start_index : end_index + 1]
        median_rolling = series.median()
        std_rolling = series.std()
        index_current = df['Index'][i]
        upper_cap, lower_cap = (median_rolling + 3 * std_rolling), (median_rolling - 3 * std_rolling)
        if index_current > upper_cap:
            index_current = upper_cap
        elif index_current < lower_cap:
            index_current = lower_cap
        else:
            pass
        zscore_current = (index_current - median_rolling) / std_rolling
        zscore.append(zscore_current)
    df['Z_Score'] = zscore
    df = df.dropna()
    # df.index = df['Date']
    return df

def Limit_Switches_Multiple (df):
    for i in range(1, len(df) - 1):
        if df.iloc[i]['phase'] != df.iloc[i-1]['phase'] and df.iloc[i]['phase'] != df.iloc[i+1]['phase'] and abs(df.iloc[i]['Z_Composite'] - df.iloc[i-1]['Z_Composite']) < 1:
            df.loc[df.index[i], 'phase']  = df.iloc[i-1]['phase']
        else:
            pass
    return df

def Identify_Phase (df_Mutiple):   

        #Initialize the data
    Phase = [np.nan]
    for i in range(1, len(df_Mutiple)):
        zscore_current = df_Mutiple.iloc[i]['Z_Composite']
        zscore_last =  df_Mutiple.iloc[i-1]['Z_Composite']
        if zscore_current >= 0 and zscore_current >= zscore_last:
            Phase.append('expansion')
        elif zscore_current >= 0 and zscore_current < zscore_last:
            Phase.append('slowdown')
        elif zscore_current <= 0 and zscore_current >= zscore_last:
            Phase.append('recovery')
        else:
            Phase.append('contraction')
    df_Mutiple['phase'] = Phase
    df_Mutiple = df_Mutiple.dropna(subset=['phase'])
    # df_Mutiple = df_Mutiple.dropna()
    df_Mutiple = Limit_Switches_Multiple(df_Mutiple)
    return df_Mutiple

def get_Data_Organization (signal_data, return_data):
    
    # South Korea has been removed as the return data is currently not available
    signal_country_name = ['Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'China', 
                           'Czech Republic', 'Denmark', 'Finland', 'France', 'Germany', 
                           'Hungary', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway',
                           'Philippines', 'Poland', 'Portugal', 'Russia', 'South Africa', 
                           'Spain', 'Sweden', 'Switzerland', 'Thailand', 
                           'Turkey', 'United Kingdom', 'United States']
    
    return_country_name = ['Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'China', 
                           'Czech Republic', 'Denmark', 'Finland', 'France', 'Germany', 
                           'Hungary', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway',
                           'Philippines', 'Poland', 'Portugal', 'Russia', 'South Africa', 
                           'Spain', 'Sweden', 'Switzerland', 'Thailand', 
                           'Turkey', 'UK', 'US']
    
    output = dict()
    
    for country in signal_country_name:
        print(country)
        for signal in signal_data[country].keys():
            signal_data[country][signal] = signal_data[country][signal].to_frame()
            signal_data[country][signal] = Get_Zscore(signal_data[country][signal])
        
        
        output[country] = [signal_data[country]['Lead Indicators']['Z_Score'], 
                           signal_data[country]['Business Sentiment']['Z_Score'], 
                           signal_data[country]['Unemployment Rate']['Z_Score'],
                           signal_data[country]['Consumer Sentiment']['Z_Score']]
        output[country]  = pd.concat(output[country] , axis = 1)
        output[country].columns = ['LI', 'BS', 'UR', 'CS']
        # Unemployment rate is an inverse indicator and need to be multiplied by -1
        output[country]['UR'] = -1 * output[country]['UR']
        Z_Composite = []
        for i in range(len(output[country])):
            current_row = output[country].iloc[i, :].dropna()
            current_len = len(current_row)
            current_zscore = sum(current_row) / current_len
            Z_Composite.append(current_zscore)
        output[country]['Z_Composite'] = Z_Composite
        output[country] = Identify_Phase(output[country])
        output[country] = output[country][output[country].index >= datetime.strptime("1990-01-15", '%Y-%m-%d')]
        
        print(output[country])
        Return = [np.nan]
        
        country_index = signal_country_name.index(country)
        country_name_return = return_country_name [country_index]
        print(country_name_return)
        country_return = return_data[country_name_return].to_frame()
        country_return.columns = ['Index']
        
        print(country_return)
        for i in range(1, len(output[country])):
            if output[country].index[i-1] < country_return.index[0]:
                Return.append(np.nan)
            else:
                index_this_month = country_return[country_return.index <= output[country].index[i]]['Index'][-1]
                index_last_month = country_return[country_return.index <= output[country].index[i-1]]['Index'][-1]
                current_return = 100 * (index_this_month - index_last_month) / index_last_month
                Return.append(current_return)
        output[country]['Return'] = Return
        output[country] = output[country].dropna(subset=['Return'])
        output[country]['Date'] = output[country].index
    return output

data_ready_to_run = get_Data_Organization(data, data_return)

def get_Panel_Estimates (data):
    country_name = ['Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'China', 
                   'Czech Republic', 'Denmark', 'Finland', 'France', 'Germany', 
                   'Hungary', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway',
                   'Philippines', 'Poland', 'Portugal', 'Russia', 'South Africa', 
                   'Spain', 'Sweden', 'Switzerland', 'Thailand', 
                   'Turkey', 'United Kingdom', 'United States']
    country_column = []
    Latest_Phase = []
    Return_1m, Return_3m, Return_6m, Return_12m, Return_18m = [], [], [], [], []
    Return_2Yr, Return_3Yr, Return_5Yr = [], [], []
    Volatility_1m, Volatility_3m, Volatility_6m, Volatility_12m, Volatility_18m = [], [], [], [], []
    Volatility_2Yr, Volatility_3Yr, Volatility_5Yr = [], [], []
    SR_1m, SR_3m, SR_6m, SR_12m, SR_18m = [], [], [], [], []
    SR_2Yr, SR_3Yr, SR_5Yr = [], [], []
    
    for i in range(len(country_name)):
        country_column.append(country_name[i])
        print(country_name[i])
        country_data = data[country_name[i]]
        country_Lastest_Phase = country_data['phase'][-1]
        Latest_Phase.append(country_Lastest_Phase)
        
        result_12m = Link_Phase_Bootstrap(country_data, 12)[country_Lastest_Phase]
        Return_12m.append(result_12m['Mean(%)'])
        Volatility_12m.append(result_12m['Standard Deviation(%)'])
        SR_12m.append(result_12m['Mean(%)'] / result_12m['Standard Deviation(%)'])
        print([Return_12m, Volatility_12m])
        
        result_18m = Link_Phase_Bootstrap(country_data, 18)[country_Lastest_Phase]
        Return_18m.append(result_18m['Mean(%)'])
        Volatility_18m.append(result_18m['Standard Deviation(%)'])
        SR_18m.append(result_18m['Mean(%)'] / result_18m['Standard Deviation(%)'])
        print([Return_18m, Volatility_18m])
        
        result_2Yr = Link_Phase_Bootstrap(country_data, 24)[country_Lastest_Phase]
        Return_2Yr.append(result_2Yr['Mean(%)'])
        Volatility_2Yr.append(result_2Yr['Standard Deviation(%)'])
        SR_2Yr.append(result_2Yr['Mean(%)'] / result_2Yr['Standard Deviation(%)'])
        print([Return_2Yr, Volatility_2Yr])

        result_3Yr = Link_Phase_Bootstrap(country_data, 36)[country_Lastest_Phase]
        Return_3Yr.append(result_3Yr['Mean(%)'])
        Volatility_3Yr.append(result_3Yr['Standard Deviation(%)'])
        SR_3Yr.append(result_3Yr['Mean(%)'] / result_3Yr['Standard Deviation(%)'])
        print([Return_3Yr, Volatility_3Yr])
        
        result_5Yr = Link_Phase_Bootstrap(country_data, 60)[country_Lastest_Phase]
        Return_5Yr.append(result_5Yr['Mean(%)'])
        Volatility_5Yr.append(result_5Yr['Standard Deviation(%)'])
        SR_5Yr.append(result_5Yr['Mean(%)'] / result_5Yr['Standard Deviation(%)'])
        print([Return_5Yr, Volatility_5Yr])
        
    output = pd.DataFrame({"Country":country_column, "Latest_Phase":Latest_Phase,
                           'Return_12m':Return_12m, 'Return_18m':Return_18m,
                           'Return_2Yr':Return_2Yr, 'Return_3Yr':Return_3Yr,
                           'Return_5Yr':Return_5Yr,'Volatility_12m':Volatility_12m, 
                           'Volatility_18m':Volatility_18m,'Volatility_2Yr':Volatility_2Yr, 
                           'Volatility_3Yr':Volatility_3Yr,'Volatility_5Yr':Volatility_5Yr,
                           'SR_12m':SR_12m, 'SR_18m':SR_18m,
                            'SR_2Yr':SR_2Yr, 'SR_3Yr':SR_3Yr,
                            'SR_5Yr':SR_5Yr})
    return output

panel_table = get_Panel_Estimates(data_ready_to_run)




root = "mtr_data .pickle"
    
with open(root, 'rb') as f:
    data = pickle.load(f)




data['US']


data['US - Signal based (incl. 4 phases)']






















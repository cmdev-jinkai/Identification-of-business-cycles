# -*- coding: utf-8 -*-
"""
Name: Results collection across different years's horizon
Author: Jinkai Zhang
Date: July 22, 2020
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

root = "timeseries.p"
    
with open(root, 'rb') as f:
    data = pickle.load(f)

data.keys()
data['US - Signal based (incl. 4 phases)']  


data['UK - Wavelets (incl. 4 phases)'].head(10)

Counter(data['UK - Wavelets (incl. 4 phases)'].phase)
Counter(data['US - Wavelets (incl. 4 phases)'].phase)

Counter(data['UK - RS-Markov (incl. 4 phases)'].phase)
Counter(data['US - RS-Markov (incl. 4 phases)'].phase)

root2 = "duration.p"
with open(root2, 'rb') as f:
    data2 = pickle.load(f)

data2.keys()
data['UK - Signal based (incl. 4 phases)']

root3 = "bootstrap.p"
with open(root3, 'rb') as f:
    data3 = pickle.load(f)

def Get_3years_Table (data_pick):
    country_name = ['JAPAN', 'US', 'UK', 'GERMANY', 'FRANCE', 'BRAZIL', 'MEXICO']
    key_name = [(i + ' - Signal based (incl. 4 phases)') for i in country_name]
    phase_list = ['expansion', 'slowdown', 'contraction', 'recovery']
    
    country_column = []
    method_column = []
    mean_column = []
    std_column = []
    Phase_column = []
    
    for i in range(len(country_name)):

        
        current_data = data_pick[key_name[i]]
        results_all = Link_Phase_Bootstrap(current_data, 36)
        for j in range(len(phase_list)):
            current_phase = phase_list[j]
            method_column.append("Signal based (incl. 4 phases)")
            country_column.append(country_name[i])
            Phase_column.append(current_phase)
            result_phase = results_all[current_phase]
            current_mean = result_phase['Mean(%)']
            current_std = result_phase['Standard Deviation(%)']
            mean_column.append(current_mean)
            std_column.append(current_std)
            print([i, j])
            print(current_mean)
            print(mean_column)
    output = pd.DataFrame({"Country":country_column, "Method":method_column,
                           'Mean':mean_column, 'Standard.Deviation':std_column,
                           "Phase":Phase_column})
    return output
           
three_year_table = Get_3years_Table(data)
three_year_table.to_csv('output_csv/visualization_return_multiple3.csv')        


def Get_Result_Table (data_pick):
    country_name = ['JAPAN', 'US', 'UK', 'GERMANY', 'FRANCE', 'BRAZIL', 'MEXICO']
    key_name = [(i + ' - Signal based (incl. 4 phases)') for i in country_name]
    estimation_year = list(np.arange(0.5 ,10.5, 0.5))
    
    country_column = []
    mean_column = []
    std_column = []
    year_column = []
    
    estimation_month = [i * 12 for i in estimation_year]
    for i in range(len(country_name)):
        
        current_data = data_pick[key_name[i]]
        current_data.Return = current_data.Return * 100
        current_phase = current_data['phase'].iloc[-1]
        for j in range(len(estimation_year)):
            country_column.append(country_name[i])
            year_column.append(estimation_year[j])
            current_month = int(estimation_month[j])
            results_all = Link_Phase_Bootstrap(current_data, current_month)
            result_phase = results_all[current_phase]
            current_mean = result_phase['Mean(%)']
            current_std = result_phase['Standard Deviation(%)']
            mean_column.append(current_mean)
            std_column.append(current_std)
            print([i, j])
            print(current_mean)
            print(mean_column)
    
    output = pd.DataFrame({"Country":country_column, "Year":year_column,
                           'Mean':mean_column, 'Standard.Deviation':std_column})
    return output

returns_panel = Get_Result_Table(data)

returns_panel.to_csv('returns_panel.csv')


root = "timeseries.p"
with open(root, 'rb') as f:
    data = pickle.load(f)
US_data = data['US - Signal based (incl. 4 phases)']

def get_BackTest (data, back_month, forward_month):
    date_column = []
    mean_column = []
    std_column = []

    for i in range(len(data)):
        print (i)
        if i >= back_month:
            print (i)
            latest_phase = data.phase[i-1]
            print (latest_phase)
            date_column.append(data["Date"][i])
            print(data["Date"][i])
            #data.Return = data.Return * 100
            data_simulation = data.iloc[(i - back_month):(i) , :]
            print(data_simulation)
            results_all = Link_Phase_Bootstrap(data_simulation, forward_month)
            result_phase = results_all[latest_phase]
            current_mean = result_phase['Mean(%)']
            current_std = result_phase['Standard Deviation(%)']
            mean_column.append(current_mean)
            std_column.append(current_std)
            print(i)
            print(current_mean)
            print(mean_column)
        else:
            pass
    output = pd.DataFrame({"Date":date_column, 'Mean':mean_column, 'Standard.Deviation':std_column})
    return output


BackTest_US = get_BackTest(US_data, 17 * 12, 36)

Multiple_US = pd.read_csv('MultipleSignal_US.csv')


BackTest_US_Multiple = get_BackTest(Multiple_US, 12 * 12, 36)




def Get_3years_Table2 (data_pick):
    country_name = [ 'US']
    key_name = [(i + ' - Signal based (incl. 2 phases)') for i in country_name]
    phase_list = ['expansion', 'contraction']
    
    country_column = []
    method_column = []
    mean_column = []
    std_column = []
    Phase_column = []
    
    for i in range(len(country_name)):

        
        current_data = data_pick[key_name[i]]
        results_all = Link_Phase_Bootstrap(current_data, 36)
        for j in range(len(phase_list)):
            current_phase = phase_list[j]
            method_column.append("Signal based (incl. 4 phases)")
            country_column.append(country_name[i])
            Phase_column.append(current_phase)
            result_phase = results_all[current_phase]
            current_mean = result_phase['Mean(%)']
            current_std = result_phase['Standard Deviation(%)']
            mean_column.append(current_mean)
            std_column.append(current_std)
            print([i, j])
            print(current_mean)
            print(mean_column)
    output = pd.DataFrame({"Country":country_column, "Method":method_column,
                           'Mean':mean_column, 'Standard.Deviation':std_column,
                           "Phase":Phase_column})
    return output
           
three_year_table = Get_3years_Table2(data)
three_year_table.to_csv('output_csv/visualization_return_multiple32.csv') 























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
data['UK - Signal based (incl. 4 phases)']
data['UK - Wavelets (incl. 4 phases)'].head(10)

Counter(data['UK - Wavelets (incl. 4 phases)'].phase)
Counter(data['US - Wavelets (incl. 4 phases)'].phase)

Counter(data['UK - RS-Markov (incl. 4 phases)'].phase)
Counter(data['US - RS-Markov (incl. 4 phases)'].phase)

root2 = "duration.p"
with open(root2, 'rb') as f:
    data2 = pickle.load(f)

data2.keys()
data2['UK - Signal based (incl. 4 phases)']

root3 = "bootstrap.p"
with open(root3, 'rb') as f:
    data3 = pickle.load(f)



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





















"""
Name: Phase Identification with Macro-Economic Conditions (Arnott et al., 2017)
Author: Jinkai Zhang
Date: July 31, 2020

Reference: Arnott, R.D., Chaves, D.B., Chow, T.M., 2017. King of the Mountain: The Shiller P/E and Macroeconomic Conditions. Journal of Portfolio Management, 44(1), 55-68.
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
import numpy as np
import datetime
from scipy.stats import norm
from scipy.stats.mstats import gmean


root_all = r"C:\Users\cmdev\Desktop\ds_raw_data\data_dict_m.pickle"

with open(root_all, 'rb') as f: 
    data_all = pickle.load(f)

data_all.keys()

data_all['BRAZIL Real GDP']

data_all['{} Consumer Prices'.format('US')]

data_all['{} Real GDP'.format("CHINA")].keys()

root_old = r"C:\Users\cmdev\Desktop\ds_raw_data\timeseries.p"
    
with open(root_old, 'rb') as f:
    data_old = pickle.load(f)

data_old.keys()
data_old['UK - Signal based (incl. 4 phases)']
data_old['UK - Wavelets (incl. 4 phases)'].head(10)


def Annual_Percentage_GDP(df):
    #APRGDP refers to Anualized Percentage Real GDP
    APRGDP = [np.nan]
    for i in range(1, len(df)):
        current_percentage = (df.RGDP[i] - df.RGDP[i-1]) / df.RGDP[i-1]
        annual_current = current_percentage * 4 * 100
        APRGDP.append(annual_current)
    df['APRGDP'] = APRGDP
    return df

def Annual_Percentage_Inflation(df):
    APINFLATION = [np.nan]
    for i in range(1, len(df)):
        current_percentage = (df.INFLATION[i] - df.INFLATION[i-1]) / df.INFLATION[i-1]
        annual_current = current_percentage * 12 * 100
        APINFLATION.append(annual_current)
    df['APINFLATION'] = APINFLATION
    return df

def Reform_Data_Macro (data_all, data_old):
    country_name = ['JAPAN', 'US', 'UK', 'GERMANY', 'FRANCE', 'BRAZIL', 'MEXICO']
    key_name = [(i + ' - Signal based (incl. 4 phases)') for i in country_name]
    data_new = dict()
    new_name = [(i + ' - Macro based') for i in country_name]
    for i in range(len(country_name)):
        data_new[new_name[i]] = data_old[key_name[i]]
    for key, df in data_new.items():
        df = df.drop(['cycles', 'regimes', 'threshold', 'phase'], axis = 1)
        #df['Date'] = df.index
        data_new[key] = df
    for i in range(len(country_name)):
        current_country = country_name[i]
        current_data = data_all['{} Consumer Prices'.format(current_country)]
        current_table = pd.DataFrame({"Date" : list(current_data.keys()), "INFLATION":list(current_data.values())})
        current_table = Annual_Percentage_Inflation(current_table)
        current_table.index = current_table['Date']
        current_table = current_table.drop(['Date'], axis = 1)
        current_key_name = new_name[i]
        current_merge = pd.merge(data_new[current_key_name], current_table, how ='left', left_index= True, right_index= True)
        data_new[current_key_name] = current_merge
    return data_new


a = Reform_Data_Macro (data_all, data_old)

a['JAPAN - Macro based'].Return[1]

a = data_all['BRAZIL Real GDP']
a.Return[1]
a.keys()
list(a.values())


b = pd.DataFrame({"Date" : list(a.keys()), "RGDP":list(a.values())})
Annual_Percentage_GDP(b)































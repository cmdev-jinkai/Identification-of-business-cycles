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


root_all = r"C:\Users\cmdev\Desktop\ds_raw_data\data_dict_m.pickle"

with open(root_all, 'rb') as f: 
    data_all = pickle.load(f)


root_old = r"C:\Users\cmdev\Desktop\ds_raw_data\timeseries.p"
    
with open(root_old, 'rb') as f:
    data_old = pickle.load(f)



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
    for i in range(len(country_name)):
        current_country = country_name[i]
        current_data = data_all['{} Real GDP'.format(current_country)]
        current_table = pd.DataFrame({"Date" : list(current_data.keys()), "RGDP":list(current_data.values())})
        current_table = Annual_Percentage_GDP(current_table)
        current_table.index = current_table['Date']
        current_table = current_table.drop(['Date'], axis = 1)
        current_key_name = new_name[i]
        current_merge = pd.merge(data_new[current_key_name], current_table, how ='left', left_index= True, right_index= True)
        data_new[current_key_name] = current_merge
    for key, df in data_new.items():
        for i in range(1, len(df)):
            current_index = df.index[i]
            if np.isnan(df.RGDP[i]):
                df.loc[current_index, 'RGDP'] = df.RGDP[i - 1]
                df.loc[current_index, 'APRGDP'] = df.APRGDP[i - 1]          
            else:
                pass
        df = df.dropna()    
        df.Return = df.Return * 100
        df = df.drop(['RGDP', 'INFLATION'], axis = 1)
        data_new[key] = df
    for key, df in data_new.items():
        phase_GDP = []
        phase_INFLATION = []
        phase = []
        low_quantile_gdp = np.quantile(df.APRGDP, 1/3)
        high_quantile_gdp = np.quantile(df.APRGDP, 2/3)
        low_quantile_inflation = np.quantile(df.APINFLATION, 1/3)
        high_quantile_inflation = np.quantile(df.APINFLATION, 2/3)
        for i in range(len(df)):
            if df.APRGDP[i] <= low_quantile_gdp:
                phase_GDP.append('Low')
            elif df.APRGDP[i] > low_quantile_gdp and df.APRGDP[i] <= high_quantile_gdp:
                phase_GDP.append('Stable')
            else:
                phase_GDP.append('High')
        for i in range(len(df)):
            if df.APINFLATION[i] <= low_quantile_inflation:
                phase_INFLATION.append('Low')
            elif df.APINFLATION[i] > low_quantile_inflation and df.APINFLATION[i] <= high_quantile_inflation:
                phase_INFLATION.append('Stable')
            else:
                phase_INFLATION.append('High')
        for i in range(len(df)):
            phase.append(phase_GDP[i] + phase_INFLATION[i])
        df['phase_GDP'] = phase_GDP
        df['phase_INFLATION'] = phase_INFLATION
        df['phase'] = phase
        df['Date'] = df.index
        data_new[key] = df
    return data_new

data_new = Reform_Data_Macro (data_all, data_old)


def Quantile_Phase_GDP (data_new):
    for key, df in data_new.items():
        df = df.drop(['APINFLATION', 'phase_GDP', 'phase_INFLATION', 'phase'], axis = 1)
        phase = []
        order = []
        no1, no2, no3 = np.quantile(df.APRGDP, 1/7), np.quantile(df.APRGDP, 2/7), np.quantile(df.APRGDP, 3/7)
        no4, no5, no6 = np.quantile(df.APRGDP, 4/7), np.quantile(df.APRGDP, 5/7), np.quantile(df.APRGDP, 6/7)
        for i in range(len(df)):
            value = df.APRGDP[i]
            if value <= no1:
                phase.append('Below ' + str(round(no1, 1)) + '%')
                order.append(1)
            elif value > no1 and value <= no2:
                phase.append(str(round(no1, 1)) + '%' + ' to ' + str(round(no2, 1)) + '%')
                order.append(2)
            elif value > no2 and value <= no3:
                phase.append(str(round(no2, 1)) + '%' + ' to ' + str(round(no3, 1)) + '%')
                order.append(3)
            elif value > no3 and value <= no4:
                phase.append(str(round(no3, 1)) + '%' + ' to ' + str(round(no4, 1)) + '%')
                order.append(4)
            elif value > no4 and value <= no5:
                phase.append(str(round(no4, 1)) + '%' + ' to ' + str(round(no5, 1)) + '%')
                order.append(5)
            elif value > no5 and value <= no6:
                phase.append(str(round(no5, 1)) + '%' + ' to ' + str(round(no6, 1)) + '%')
                order.append(6)
            elif value > no6:
                phase.append('Above ' + str(round(no6, 1)) + '%')
                order.append(7)
            else:
                pass
        df['phase'] = phase
        df['order'] = order
        data_new[key] = df
    return data_new

data_gdp = Quantile_Phase_GDP (data_new)
data_new = Reform_Data_Macro (data_all, data_old)

def Quantile_Phase_INFLATION (data_new):
    for key, df in data_new.items():
        df = df.drop(['APRGDP', 'phase_GDP', 'phase_INFLATION', 'phase'], axis = 1)
        phase = []
        order = []
        no1, no2, no3 = np.quantile(df.APINFLATION, 1/7), np.quantile(df.APINFLATION, 2/7), np.quantile(df.APINFLATION, 3/7)
        no4, no5, no6 = np.quantile(df.APINFLATION, 4/7), np.quantile(df.APINFLATION, 5/7), np.quantile(df.APINFLATION, 6/7)
        for i in range(len(df)):
            value = df.APINFLATION[i]
            if value <= no1:
                phase.append('Below ' + str(round(no1, 1)) + '%')
                order.append(1)
            elif value > no1 and value <= no2:
                phase.append(str(round(no1, 1)) + '%' + ' to ' + str(round(no2, 1)) + '%')
                order.append(2)
            elif value > no2 and value <= no3:
                phase.append(str(round(no2, 1)) + '%' + ' to ' + str(round(no3, 1)) + '%')
                order.append(3)
            elif value > no3 and value <= no4:
                phase.append(str(round(no3, 1)) + '%' + ' to ' + str(round(no4, 1)) + '%')
                order.append(4)
            elif value > no4 and value <= no5:
                phase.append(str(round(no4, 1)) + '%' + ' to ' + str(round(no5, 1)) + '%')
                order.append(5)
            elif value > no5 and value <= no6:
                phase.append(str(round(no5, 1)) + '%' + ' to ' + str(round(no6, 1)) + '%')
                order.append(6)
            elif value > no6:
                phase.append('Above ' + str(round(no6, 1)) + '%')
                order.append(7)
            else:
                pass
        df['phase'] = phase
        df['order'] = order
        data_new[key] = df
    return data_new

data_inflation= Quantile_Phase_INFLATION (data_new)
data_new = Reform_Data_Macro (data_all, data_old)


def Get_Univariate_Comparison (data_gdp, data_inflation, month):
    country_name = ['US', 'UK', 'GERMANY', 'FRANCE', 'BRAZIL', 'MEXICO']
    key_name = [(i + ' - Macro based') for i in country_name]
    country_column = []
    phase_gdp = []
    phase_inflation = []
    mean_column_gdp = []
    std_column_gdp = []
    phase_inflation = []
    mean_column_inflation = []
    std_column_inflation = []
    for i in range(len(country_name)):
        df_gdp = data_gdp[key_name[i]]
        df_inflation = data_inflation[key_name[i]]
        phase_gdp_list = list(df_gdp.sort_values(by=['order'])['phase'].drop_duplicates())
        phase_inflation_list = list(df_inflation.sort_values(by=['order'])['phase'].drop_duplicates())
        results_all = Link_Phase_Bootstrap(df_gdp, month)
        for j in range(len(phase_gdp_list)):
            current_phase = phase_gdp_list[j]
            country_column.append(country_name[i])
            phase_gdp.append(current_phase)
            result_phase = results_all[current_phase]
            current_mean = result_phase['Mean(%)']
            current_std = result_phase['Standard Deviation(%)']
            mean_column_gdp.append(current_mean)
            std_column_gdp.append(current_std)
            print([i, j])
            print(current_mean)
        results_all = Link_Phase_Bootstrap(df_inflation, month)
        for j in range(len(phase_inflation_list)):
            current_phase = phase_inflation_list[j]
            phase_inflation.append(current_phase)
            result_phase = results_all[current_phase]
            current_mean = result_phase['Mean(%)']
            current_std = result_phase['Standard Deviation(%)']
            mean_column_inflation.append(current_mean)
            std_column_inflation.append(current_std)
            print([i, j])
            print(current_mean)
    output = pd.DataFrame({"Country":country_column, "phase_gdp":phase_gdp,
                           'Mean_GDP':mean_column_gdp, 'Standard.Deviation_GDP':std_column_gdp, "phase_inflation":phase_inflation,
                           'Mean_INFLATION':mean_column_inflation, 'Standard.Deviation_INFLATION':std_column_inflation})
    return output

result_one_year = Get_Univariate_Comparison (data_gdp, data_inflation, 12)

result_one_year.to_csv('output_macro_csv/result_one_year.csv')

def Get_US(df):
    country = ['US' for i in range(9)]
    phase_list = list(df['phase'].drop_duplicates())
    Return = []
    results_all = Link_Phase_Bootstrap(df, 12)
    for i in range(len(phase_list)):
        current_phase = phase_list[i]
        result_phase = results_all[current_phase]
        current_mean = result_phase['Mean(%)']
        Return.append(current_mean)
    output = pd.DataFrame({"Country":country, "phase_list":phase_list,
                           'Return':Return})
    return output
    
trail_US = Get_US(data_new['US - Macro based'])
trail_US.to_csv("3D_us.csv")

with open('data_new.pickle', 'wb') as handle:
    pickle.dump(data_new, handle, protocol=pickle.HIGHEST_PROTOCOL)






























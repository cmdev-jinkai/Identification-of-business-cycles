# -*- coding: utf-8 -*-
"""
Name: Results estimates over different horizons for 41 countries Using Three Methods Individually
Author: Jinkai Zhang
Date: October 20-21, 2020

Description: This version is used for monthly update of MTR for 41 countries (can be extended given all data in same format)

Monthly Data input: "mtr_data.pickle"    
Components of the input: 
    Seven time series for 41 countries, (albert 5 countries may miss some series), which are
    1. Makrt Index; 2. Unemployment Rate; 3. Consumer Sentiment; 4. Business Sentiment;
    5. Lead Indicators; 6. GDP; 7. CPI 
    note: all these data belong to raw data, and transforms are already contained in the function

Steps of Monthly update:
    1. Put pickle data 'mtr_data.pickle' in working directory, in which the NAME and DATA type are 100% matched with this version;
    2. Activate all the package, function and class;
    3. run the code line 557-561;
    4. Check the three output files in working directory (2 hours running time for each).
    
Note:
    1. For signal-based approach, if the output of few countries not appear, it is due to the data missing issue in pickle;
       e.g. the OECD Lead indicator is missing for Columbia
    2. For the macro-based approach, if the output of few countries not appear, it is due to that CPI series is not monthly;
       e.g. the case in AUSTRALIA
    
"""

import pickle
import pandas as pd
import numpy as np
import random
import statsmodels.api as sm
from datetime import datetime


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~ Novel Bootstrap Approach ~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

def bootstrap (returns, periods_month, method = 'NED', condidence_interval = 95):
    try:    
 
        #method of NED, sampled from normal distribution
        if method == 'NED':
            #mean and standard deviation of historical culmulative return
            mu_NED = np.array(returns).mean()
            sigma_NED = np.array(returns).std()
            mean_collection = []
            std_collection = []
            median_collection = []
            twentyfive_collection = []
            seventyfive_collection = []
            confi_string =  'Confidence Interval(' + str(condidence_interval) + ')(%)'
            confi_right = condidence_interval
            confi_left = 100 - confi_right
            left_collection = []
            right_collection = []
            
            #repeat each simulation of sampling 100000 monthly returns for 1000 times, consistent with Fama and French (2018).
            for i in range(1000):
                #base sample selected from normal distribution with same mean and std in real month data
                data_application = np.random.normal(mu_NED, sigma_NED, 100000)
                
                mean_collection.append(np.mean(data_application))
                std_collection.append(np.std(data_application))
                median_collection.append(np.median(data_application))
                twentyfive_collection.append(np.percentile(data_application, 25))
                seventyfive_collection.append(np.percentile(data_application, 75))
                left_collection.append(np.percentile(data_application, confi_left))
                right_collection.append(np.percentile(data_application, confi_right))
           
            output = dict()
            output['Mean(%)'] = round(np.mean(mean_collection), 4)
            output['Standard Deviation(%)'] = round(np.mean(std_collection), 4)
            output['Median(%)'] = round(np.mean(median_collection), 4)
            output['25th(%)'] = round(np.mean(twentyfive_collection), 4)
            output['75th(%)'] = round(np.mean(seventyfive_collection), 4)
            output[confi_string] = [round(np.mean(left_collection), 4),
                                   round(np.mean(right_collection), 4)]  
            
            #please run 'return output['Mean(%)']' if only need output of return
            return output
       
        elif method == 'FS':
            mean_collection = []
            std_collection = []
            median_collection = []
            twentyfive_collection = []
            seventyfive_collection = []
            confi_string =  'Confidence Interval(' + str(condidence_interval) + ')(%)'
            confi_right = condidence_interval
            confi_left = 100 - confi_right
            left_collection = []
            right_collection = []
            
            for i in range(1000):
            #base sample selected from real monthly return data
                data_application = random.choices(returns, k = 100000)
                mean_collection.append(np.mean(data_application))
                std_collection.append(np.std(data_application))
                median_collection.append(np.median(data_application))
                twentyfive_collection.append(np.percentile(data_application, 25))
                seventyfive_collection.append(np.percentile(data_application, 75))
                left_collection.append(np.percentile(data_application, confi_left))
                right_collection.append(np.percentile(data_application, confi_right))
                
            output = dict()
            output['Mean(%)'] = round(np.mean(mean_collection), 4)
            output['Standard Deviation(%)'] = round(np.mean(std_collection), 4)
            output['Median(%)'] = round(np.mean(median_collection), 4)
            output['25th(%)'] = round(np.mean(twentyfive_collection), 4)
            output['75th(%)'] = round(np.mean(seventyfive_collection), 4)
            output[confi_string] = [round(np.mean(left_collection), 4),
                                   round(np.mean(right_collection), 4)]  
            
            #please run 'return output['Mean(%)']' if only need output of return
            return output
        else:
            print ('Oops! The method is not included..')
    except:
        print('Oops! Something wrong. May check the column name and try again..')

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



"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~ Multiple Signal-Based Approach ~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# Function to calculate rolling 3 years Z-score
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

def get_Data_Signal (signal_data):
    
    # here list all countries for transparency, can be replaced by code $list(signal_data.keys())$ in future
    signal_country_name = ['AUSTRALIA', 'AUSTRIA', 'BELGIUM', 'BRAZIL', 'CANADA', 'CHILE', 'CHINA', 
                           'COLOMBIA', 'CZECH REPUBLIC', 'DENMARK', 'FINLAND', 'FRANCE', 'GERMANY', 
                           'GREECE', 'HONG KONG', 'HUNGARY', 'INDIA', 'INDONESIA', 'IRELAND', 'ISRAEL',
                           'ITALY', 'JAPAN', 'KOREA', 'MEXICO', 'NETHERLANDS', 'NEW ZEALAND', 'NORWAY', 
                           'PHILIPPINES', 'POLAND', 'PORTUGAL', 'RUSSIA', 'SINGAPORE', 'SOUTH AFRICA', 
                           'SPAIN', 'SWEDEN', 'SWITZERLAND', 'TAIWAN', 'THAILAND', 'TURKEY', 'UK', 'US']
    
    
    output = dict()
    signal_key = ['Unemployment', 'Consumer Sentiment', 'Business Sentiment', 'Lead Indicators', 'GDP', 'CPI']
    for country in signal_country_name:
        if len(list(signal_data[country].keys())) == 7 :
            print("Currently working for data management for---" + country + "----.")
            for signal in signal_key:
                signal_data[country][signal] = signal_data[country][signal].to_frame()
                signal_data[country][signal] = Get_Zscore(signal_data[country][signal])
            
            
            output[country] = [signal_data[country]['Lead Indicators']['Z_Score'], 
                               signal_data[country]['Business Sentiment']['Z_Score'], 
                               signal_data[country]['Unemployment']['Z_Score'],
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
            output[country] = output[country][output[country].index >= datetime.strptime("1980-01-15", '%Y-%m-%d')]
            

            Return = [np.nan]
            
            country_index = signal_country_name.index(country)
            country_name_return = signal_country_name [country_index]

            country_return = signal_data[country_name_return]['Market'].to_frame()
            country_return.columns = ['Index']
            

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
        else:
            print("Some data missing for " + country + ". Please have a double check.")
            pass
    print("Data management for signal-based approach is completed and thereafter proceed on estimation..")
    return output




def get_Estimates_ALL (data):
    country_name = list(data.keys())
    country_column = []
    Latest_Phase = []
    #Return_1m, Return_3m, Return_6m, 
    Return_12m, Return_18m = [], []
    Return_2Yr, Return_3Yr, Return_5Yr = [], [], []
    #Volatility_1m, Volatility_3m, Volatility_6m, 
    Volatility_12m, Volatility_18m = [], []
    Volatility_2Yr, Volatility_3Yr, Volatility_5Yr = [], [], []
    #SR_1m, SR_3m, SR_6m, 
    SR_12m, SR_18m = [], []
    SR_2Yr, SR_3Yr, SR_5Yr = [], [], []
    
    for i in range(len(country_name)):
        country_column.append(country_name[i])
        print("Return Estimation started for ---" + country_name[i] + "---.")
        country_data = data[country_name[i]]
        country_Lastest_Phase = country_data['phase'][-1]
        Latest_Phase.append(country_Lastest_Phase)
        
        result_12m = Link_Phase_Bootstrap(country_data, 12)[country_Lastest_Phase]
        Return_12m.append(result_12m['Mean(%)'])
        Volatility_12m.append(result_12m['Standard Deviation(%)'])
        SR_12m.append(result_12m['Mean(%)'] / result_12m['Standard Deviation(%)'])
        
        result_18m = Link_Phase_Bootstrap(country_data, 18)[country_Lastest_Phase]
        Return_18m.append(result_18m['Mean(%)'])
        Volatility_18m.append(result_18m['Standard Deviation(%)'])
        SR_18m.append(result_18m['Mean(%)'] / result_18m['Standard Deviation(%)'])
        
        result_2Yr = Link_Phase_Bootstrap(country_data, 24)[country_Lastest_Phase]
        Return_2Yr.append(result_2Yr['Mean(%)'])
        Volatility_2Yr.append(result_2Yr['Standard Deviation(%)'])
        SR_2Yr.append(result_2Yr['Mean(%)'] / result_2Yr['Standard Deviation(%)'])

        result_3Yr = Link_Phase_Bootstrap(country_data, 36)[country_Lastest_Phase]
        Return_3Yr.append(result_3Yr['Mean(%)'])
        Volatility_3Yr.append(result_3Yr['Standard Deviation(%)'])
        SR_3Yr.append(result_3Yr['Mean(%)'] / result_3Yr['Standard Deviation(%)'])
       
        result_5Yr = Link_Phase_Bootstrap(country_data, 60)[country_Lastest_Phase]
        Return_5Yr.append(result_5Yr['Mean(%)'])
        Volatility_5Yr.append(result_5Yr['Standard Deviation(%)'])
        SR_5Yr.append(result_5Yr['Mean(%)'] / result_5Yr['Standard Deviation(%)'])
        
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


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~ Macro-economics Condition Based Approach ~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

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

def get_Data_Macro (macro_data):
    country_name =  list(macro_data.keys())
    output = dict()
    for country in country_name:
        if (macro_data[country]['CPI'].index[1] - macro_data[country]['CPI'].index[0]).days < 45:
            print("Currently working for data management for---" + country + "----.")           
            macro_data[country]['CPI'] = macro_data[country]['CPI'].to_frame()
            macro_data[country]['CPI'].columns = ['INFLATION']
            macro_data[country]['CPI'] = Annual_Percentage_Inflation(macro_data[country]['CPI'])
            macro_data[country]['GDP'] = macro_data[country]['GDP'].to_frame()
            macro_data[country]['GDP'].columns = ['RGDP']
            macro_data[country]['GDP'] = Annual_Percentage_GDP(macro_data[country]['GDP'])
            output[country] = [macro_data[country]['GDP']['APRGDP'], macro_data[country]['CPI']['APINFLATION']]
            output[country]  = pd.concat(output[country] , axis = 1)
            output[country] = output[country].dropna(subset=['APINFLATION'])
            for i in range(1, len(output[country])):
                current_index = output[country].index[i]
                if np.isnan(output[country].APRGDP[i]):
                    output[country].loc[current_index, 'APRGDP'] = output[country].APRGDP[i - 1]          
                else:
                    pass
            output[country] = output[country].dropna(subset=['APRGDP'])
            
            phase_GDP = []
            phase_INFLATION = []
            phase = []
            quantile_gdp = np.quantile(output[country].APRGDP, 1/2)
            quantile_inflation = np.quantile(output[country].APINFLATION, 1/2)
            for i in range(len(output[country])):
                if output[country].APRGDP[i] <= quantile_gdp:
                    phase_GDP.append('LowGDP')
                else:
                    phase_GDP.append('HighGDP')
            for i in range(len(output[country])):
                if output[country].APINFLATION[i] <= quantile_inflation:
                    phase_INFLATION.append('LowInflation')
                else:
                    phase_INFLATION.append('HighInflation')
            for i in range(len(output[country])):
                phase.append(phase_GDP[i] + '&' + phase_INFLATION[i])
            output[country]['phase_GDP'] = phase_GDP
            output[country]['phase_INFLATION'] = phase_INFLATION
            output[country]['phase'] = phase
            
            country_return = macro_data[country]['Market'].to_frame()
            country_return.columns = ['Index']
            
            Return = [np.nan]

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
        else:
            print("The CPI data might be not monthly for ---" + country + "---.Please have a double check.")
            pass
    print("Data management for macro-based approach is completed and thereafter proceed on estimation..")
    return output

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~ Regime-Switching Based Approach ~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
def get_Data_RS (rs_data):
    country_name =  list(rs_data.keys())
    date_series = rs_data['US']['CPI'].index
    output = dict()
    for country in country_name:
        print("Currently working for data management for---" + country + "----.")
        output[country] = pd.DataFrame(columns = ["Date"])
        output[country] = output[country].append(pd.DataFrame({"Date" : date_series}))
        output[country].index = date_series
        country_return = rs_data[country]['Market'].to_frame()
        country_return.columns = ['Index']
            
        Return = [np.nan]
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
        
        model_rs = sm.tsa.MarkovAutoregression(output[country]['Return'], k_regimes = 3, trend = 'c',
                                          order = 1, switching_ar = True, switching_variance = True)
        fit_rs = model_rs.fit()
        phase = []
        prob_table = fit_rs.filtered_marginal_probabilities
        for i in range(len(prob_table)):
            current_row = prob_table.iloc[1, :]
            index_phase = list(current_row).index(max(current_row))
            if index_phase == 0:
                phase.append("Risk off")
            elif index_phase == 1:
                phase.append("Neutral")
            else:
                phase.append("Risk on")
        prob_table['phase'] = phase
        Return = []
        for i in range(len(prob_table)):
            current_index = prob_table.index[i]
            Return.append(output[country].loc[current_index, 'Return'])
        prob_table['Return'] = Return
        output[country] = prob_table
    print("Data management for RS-based approach is completed and thereafter proceed on estimation..")
    return output
        
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~ Monthly Update Class ~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

class MTR_Update:
    
    def __init__(self, root):
      self.root = root

    def Initialization(self):
        with open(self.root, 'rb') as f:
            data = pickle.load(f)
        self.data = data
    
    def Signal_Based(self):
        self.Initialization()
        data_ready_to_run_signal = get_Data_Signal(self.data)
        panel_table_signal = get_Estimates_ALL (data_ready_to_run_signal)
        panel_table_signal.to_csv('panel_table_signal.csv')
        print("Signal-Based Estimation Completed. Please Check The Output.")
    
    def Macro_Based(self):
        self.Initialization()
        data_ready_to_run_macro = get_Data_Macro (self.data)
        panel_table_macro = get_Estimates_ALL (data_ready_to_run_macro)
        panel_table_macro.to_csv('panel_table_macro.csv')
        print("Macro-Based Estimation Completed. Please Check The Output.")
    
    # RS refers to Makov Chain Regime Swiching
    def RS_Based(self):
        self.Initialization()
        data_ready_to_run_rs = get_Data_RS (self.data)
        panel_table_rs = get_Estimates_ALL (data_ready_to_run_rs)
        panel_table_rs.to_csv('panel_table_rs.csv')
        print("RS-Based Estimation Completed. Please Check The Output.")
        
if __name__ == '__main__':
    
    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ Outputs ~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    
    root = "mtr_data.pickle"
    Monthly_Update = MTR_Update(root)
    Monthly_Update.Signal_Based()
    Monthly_Update.Macro_Based()
    Monthly_Update.RS_Based()
    
    
    
    '''
    Alternative way of updates without using class
    # READ MONTHLY DATA
    root = "mtr_data.pickle"    
    with open(root, 'rb') as f:
        data = pickle.load(f)
    # MULTIPLE SIGNAL BASED
    data_ready_to_run_signal = get_Data_Signal(data)
    panel_table_signal = get_Estimates_ALL (data_ready_to_run_signal)
    panel_table_signal.to_csv('panel_table_signal.csv')
    
    
    # RE-READ MONTHLY DATA
    root = "mtr_data.pickle"    
    with open(root, 'rb') as f:
        data = pickle.load(f)    
    # MACROECONOMIC CONDITION BASED
    data_ready_to_run_macro = get_Data_Macro (data)
    panel_table_macro = get_Estimates_ALL (data_ready_to_run_macro)
    panel_table_macro.to_csv('panel_table_macro.csv')

    
    # RE-READ MONTHLY DATA
    root = "mtr_data.pickle"    
    with open(root, 'rb') as f:
        data = pickle.load(f)    
    # REGIME-SWITCHING
    data_ready_to_run_rs = get_Data_RS (data)
    panel_table_rs = get_Estimates_ALL (data_ready_to_run_rs)
    panel_table_rs.to_csv('panel_table_rs.csv')
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import pandas as pd
import numpy as np
import random




def bootstrap (returns, periods_month, method = 'NED', condidence_interval = 95):
    try:    
        #this function calculated the cumulated LTR based on extracting required number of monthly returns from 100000 numbers according to the time horizon
        def LT_Return (series):
            #sample required number of monthly returns from 100000 returns
            LTR = random.choices(series, k = periods_month)
            def plus_one (x): return (x/100 + 1)
            LTR = list(map(plus_one, LTR))
            #culmulate the monthly return to LTR
            Cumul_Ret = np.prod(LTR) - 1
            
            #Transfer from Cumulated return to Anualized return
            # (1 + Montly_Return) ^ periods_month - 1 = Cumul_Ret    ----(1)
            Montly_Return = (Cumul_Ret + 1) ** (1 / periods_month) - 1
            # (1 + Montly_Return) ^ 12 - 1 = Anualized_Return    ----(2)
            Anualized_Return = (1 + Montly_Return) ** 12 - 1
            
            #transfer back to the unit of '%'
            Anualized_Return = Anualized_Return * 100
            return Anualized_Return
        
        #this function provide the structure of output, to be shown in a dictionary
        def get_output (data):
            output = dict()
            output['Mean(%)'] = round(np.mean(data), 4)
            output['Standard Deviation(%)'] = round(np.std(data), 4)
            output['Median(%)'] = round(np.median(data), 4)
            output['25th(%)'] = round(np.percentile(data, 25), 4)
            output['75th(%)'] = round(np.percentile(data, 75), 4)
            confi_string =  'Confidence Interval(' + str(condidence_interval) + ')(%)'
            confi_right = condidence_interval
            confi_left = 100 - confi_right
            output[confi_string] = [round(np.percentile(data, confi_left), 4),
                                   round(np.percentile(data, confi_right), 4)]
            return output
        #method of NED, sampled from normal distribution
        if method == 'NED':
            #mean and standard deviation of historical monthly returns
            mu_NED = np.array(returns).mean()
            sigma_NED = np.array(returns).std()
            data_simulation = []
            #repeat each simulation of sampling 100000 monthly returns for 1000 times, consistent with Fama and French (2018).
            for i in range(1000):
                #base sample selected from normal distribution with same mean and std in real month data
                data_application = np.random.normal(mu_NED, sigma_NED, 100000)
                data_simulation.append(data_application)
            data_LTR = list(map(LT_Return, data_simulation))
            return get_output(data_LTR)
       
        elif method == 'FS':
            data_simulation = []
            for i in range(1000):
            #base sample selected from real monthly return data
                data_application = random.choices(returns, k = 100000)
                data_simulation.append(data_application)
            data_LTR = list(map(LT_Return, data_simulation))
            return get_output(data_LTR)
        else:
            print ('Oops! The method is not included..')
    except:
        print('Oops! Something wrong. May check the column name and try again..')

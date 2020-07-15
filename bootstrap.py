'''
Name:Bootstrap method in estimation of returns (Fama and French, 2018)
Author: Jinkai Zhang
Date: May 20, 2020

This method provides a new estimation complementary to Averaged Historical Returns Advantages: 
    1) Realized data become less available in long-term; 
    2) No restriction to historical data; 3) simplify the distribution

Assumptions: 
    1.Monthly return is a process of random walk; 
    2.Long-term return is the product of monthly return; 
    3.The central limit theorem says bootstraped LTR converge toward nomal distribution;

There are two sub-methods called NED and FS: 
    1. NED: monthly return sampled from normal distribution with the same mean and standard deviation of historical return; 
    2. FS: monthly return sampled directly from historical return.

Steps: 
    1. sample these monthly returns with replacement to generate each horizon’s 100,000 cumulative returns 
    2. repeat the process by 1000 times 
    3. calculate the statistical information

Reference: 
    Fama E.F. and French, K.R., 2018. Long-horizon returns. The Review of Asset Pricing Studies, 8(2), 232-252.
    Link: https://academic.oup.com/raps/article-abstract/8/2/232/4810768

'''

import pandas as pd
import numpy as np
import random




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

# Identification-of-business-cycles
Name:Identification of cycles with different number of phases
Author: Jinkai Zhang
Date: June 23, 2020
Description:
    This file provides the functions to identify the business cycles while allowing users to choose the number of total cycles
    The methods are application to the other time series data in the identification of cycles
    There are three types of phases identification included which are:
        Two phases identication: 'Expansion', 'Recession'
        Four phases identification: "Expansion", "Slowdown","Recession", "Recovery"
        Six phases identification: "Expansion", "Slowdown","Recession", "Recovery", "DoubleUp", "DoubleDown"
    
Logic of the idenfication in Two phases:
    1. Two phases identification is straightford depending on whether the index above/below mean (e.g. 100 in OECD data)
    
Logic of the idenfication in Four phases:
    1. Identify all the peaks with the mark of '+' and '-' representing up and down peak
    2. In time series data, if two or more consecutive '+'/'-' peak identified, we choose the most evident peak, allowing up and down peak appears alternatively
    3. Use the time point of peak and whether it is above mean to determine the position of cycle

Logic of the idenfication in Six phases:
    1. logis of six phases are based on four phase;
    2. In point 2 of logic to identify four phase, if two consecutive '+' are observed as peak, the period in these two shall be identified as 'DoubleUp' phase
    3. Similar application to 'DoubleDown' phase
    4. adjust the existing months in four phase

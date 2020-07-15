'''
Name:Plot the phases with different color
Author: Jinkai Zhang
Date: July 15, 2020
'''
install.packages("ggplot2")
library(ggplot2)
library(scales)

setwd("GitHub/Identification-of-business-cycles")

#read data
SingleInput_2Phases = read.csv('output_csv/SingleInput_2Phases.csv')
SingleInput_4Phases = read.csv('output_csv/SingleInput_4Phases.csv')
SingleInput_6Phases = read.csv('output_csv/SingleInput_6Phases.csv')

MultipleInput_2Phases =  read.csv('output_csv/MultipleInput_2Phases.csv')
MultipleInput_4Phases =  read.csv('output_csv/MultipleInput_4Phases.csv')
MultipleInput_6Phases =  read.csv('output_csv/MultipleInput_6Phases.csv')

#select required columns
SingleInput_2Phases = SingleInput_2Phases[, c(2,4,5)]
SingleInput_4Phases = SingleInput_4Phases[, c(2,4,5)]
SingleInput_6Phases = SingleInput_6Phases[, c(2,4,7)]

MultipleInput_2Phases = MultipleInput_2Phases[, c(2,8,9)]
MultipleInput_4Phases = MultipleInput_4Phases[, c(2,8,9)]
MultipleInput_6Phases = MultipleInput_6Phases[, c(2,8,11)]

#Single Input
ggplot(SingleInput_2Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Two using OECD input (1964-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")

ggplot(SingleInput_4Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Four using OECD input (1964-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")

ggplot(SingleInput_6Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Six using OECD input (1964-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")

#Multiple inputs
ggplot(MultipleInput_2Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Composite, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Two using multiple inputs (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")

ggplot(MultipleInput_4Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Composite, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Four using multiple inputs (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")

ggplot(MultipleInput_6Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Composite, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Six using multiple inputs (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")

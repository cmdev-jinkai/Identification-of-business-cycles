'''
Name:Plot the phases with different color
Author: Jinkai Zhang
Date: July 15, 2020
'''
install.packages("ggplot2")
library(ggplot2)

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
SingleInput_6Phases = SingleInput_6Phases[, c(2,4,5)]

MultipleInput_2Phases = MultipleInput_2Phases[, c(2,8,9)]
MultipleInput_4Phases = MultipleInput_4Phases[, c(2,8,9)]
MultipleInput_6Phases = MultipleInput_6Phases[, c(2,8,9)]

ggplot(SingleInput_2Phases, aes(Date, Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Two using OECD input (1964-2020)")
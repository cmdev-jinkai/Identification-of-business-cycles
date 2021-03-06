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
MultipleInput_4Phases =  read.csv('output_csv/PhaseAugust.csv')
MultipleInput_6Phases =  read.csv('output_csv/MultipleInput_6Phases.csv')

#select required columns
SingleInput_2Phases = SingleInput_2Phases[, c(2,4,5)]
SingleInput_4Phases = SingleInput_4Phases[, c(2,4,5)]
SingleInput_6Phases = SingleInput_6Phases[, c(2,4,7)]

MultipleInput_2Phases = MultipleInput_2Phases[, c(2,8,9)]
MultipleInput_4Phases = MultipleInput_4Phases[, c(2,8,9)]
MultipleInput_6Phases = MultipleInput_6Phases[, c(2,8,11)]

head(SingleInput_4Phases)
head(MultipleInput_4Phases)
#Single Input
SingleInput_2phase = ggplot(SingleInput_2Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Two using OECD input (1964-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month") +
  theme_bw() +
  scale_color_manual(values = c("expansion" = "blue", "contraction" = "red"))

ggsave("output_jpg/visualization_phase//SingleInput_2phase.png")

SingleInput_4phase = ggplot(SingleInput_4Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  #labs(title = "Phase Identification in Four using OECD input (1964-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month", y = "Z-score Transform") +
  scale_y_discrete(limits=-5:3) +
  theme_bw() +
  scale_x_date(date_breaks = "10 year",
               date_labels = "%m-%Y") +
  theme(legend.position="bottom", panel.grid.major = element_blank(),panel.grid.minor = element_blank()) +
  theme(axis.text=element_text(size=12), axis.title=element_text(size=12)) +
  theme(legend.text=element_text(size=12)) +
  scale_color_manual(values = c("expansion" = "blue", "contraction" = "red", "recovery" = "green",
                                "slowdown" = "black")) 

ggsave("output_jpg/visualization_phase//SingleInput_4phase.png")


SingleInput_6phase = ggplot(SingleInput_6Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Score, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Six using OECD input (1964-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month") +
  theme_bw() +
  scale_color_manual(values = c("expansion" = "blue", "contraction" = "red", "recovery" = "yellow2",
                                "slowdown" = "black", "re-acceleration" = "pink","double_dip" = "darkcyan"))

ggsave("output_jpg/visualization_phase//SingleInput_6phase.png")
#Multiple inputs
MultipleInput_2phase = ggplot(MultipleInput_2Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Composite, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Two using multiple inputs (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month")+
  theme_bw() +
  scale_color_manual(values=c("red", "blue")) +
  scale_color_manual(values = c("expansion" = "blue", "contraction" = "red"))

ggsave("output_jpg/visualization_phase//MultipleInput_2phase.png")

MultipleInput_4Phases = na.omit(MultipleInput_4Phases)

MultipleInput_4phase = 
  ggplot(MultipleInput_4Phases, aes(as.Date(Date, format = "%m/%d/%Y"), Z_Composite, colour = phase)) + 
  geom_line(aes(group = 1)) +
  #labs(title = "Phase Identification in Four using multiple inputs (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month", y = "Composite Z-score") +
  theme_bw() +
  scale_x_date(date_breaks = "4 year",
               date_labels = "%m-%Y") +
  theme(legend.position="bottom", panel.grid.major = element_blank(),panel.grid.minor = element_blank()) +
  theme(axis.text=element_text(size=12), axis.title=element_text(size=12)) +
  theme(legend.text=element_text(size=12)) +
  scale_color_manual(values = c("expansion" = "blue", "contraction" = "red", "recovery" = "green",
                                "slowdown" = "black"))

ggsave("output_jpg/visualization_phase//MultipleInput_4phase.png")

MultipleInput_6phase = ggplot(MultipleInput_6Phases, aes(as.Date(Date, format = "%Y-%m-%d"), Z_Composite, colour = phase)) + 
  geom_line(aes(group = 1)) +
  labs(title = "Phase Identification in Six using multiple inputs (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month") +
  theme_bw() +
  scale_color_manual(values = c("expansion" = "blue", "contraction" = "red", "recovery" = "yellow2",
                                "slowdown" = "black", "re-acceleration" = "pink","double_dip" = "darkcyan"))

ggsave("output_jpg/visualization_phase//MultipleInput_6phase.png")

all_phase_figure =
  multiplot(SingleInput_4phase, SingleInput_6phase, MultipleInput_4phase, MultipleInput_6phase, cols = 2)

'''
Name:Plot the  bubble chart for different countries
Author: Jinkai Zhang
Date: July 22, 2020

'''
setwd("GitHub/Identification-of-business-cycles")

library(ggplot2)

return_all = read.csv('output_csv/visualization_return_multiple.csv')

Reform_Table = function(x){
  x$Mean = x$Mean * 100
  x$Standard.Deviation = x$Standard.Deviation * 100
  Sharp.Ratio = x$Mean / x$Standard.Deviation
  x = data.frame(x, Sharp.Ratio = Sharp.Ratio)
  return(x)
}

return_all = Reform_Table(return_all)
return_phase_four = subset(return_all, Method == 'Wavelets (incl. 4 phases)') 

return_phase_expansion = subset(return_phase_four, Phase == 'expansion')
return_phase_contraction = subset(return_phase_four, Phase == 'contraction')
return_phase_recovery = subset(return_phase_four, Phase == 'recovery')
return_phase_slowdown = subset(return_phase_four, Phase == 'slowdown')


expansion_figure =
  ggplot(return_phase_expansion, aes(y = Mean, x = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Expansion Phase") +
  ylab("Mean of Annualized Return (%)") +
  xlab("Standard Deviation (%)") +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(5, 15)) +
  theme_bw() +
  theme(
    plot.title = element_text(color = "black", size = 12),
    plot.subtitle = element_text(color = "blue", face = "bold"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )

ggsave("output_jpg/visualization_bubble//expansion_figure.png")

slowdown_figure =
  ggplot(return_phase_slowdown, aes(y = Mean, x = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Slowdown Phase") +
  ylab("Mean of Annualized Return (%)") +
  xlab("Standard Deviation (%)") +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(5, 15)) +
  theme_bw() +
  theme(
    plot.title = element_text(color = "black", size = 12),
    plot.subtitle = element_text(color = "blue", face = "bold"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )

ggsave("output_jpg/visualization_bubble//slowdown_figure.png")

contraction_figure =
  ggplot(return_phase_contraction, aes(y = Mean, x = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Contraction Phase") +
  ylab("Mean of Annualized Return (%)") +
  xlab("Standard Deviation (%)") +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(5, 15)) +
  theme_bw() +
  theme(
    plot.title = element_text(color = "black", size = 12),
    plot.subtitle = element_text(color = "blue", face = "bold"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )

ggsave("output_jpg/visualization_bubble//contraction_figure.png")


recovery_figure =
  ggplot(return_phase_recovery, aes(y = Mean, x = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Recovery Phase") +
  ylab("Mean of Annualized Return (%)") +
  xlab("Standard Deviation (%)") +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(5, 15)) +
  theme_bw() +
  theme(
    plot.title = element_text(color = "black", size = 12),
    plot.subtitle = element_text(color = "blue", face = "bold"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )


all_phase_figure_wave =
  multiplot(expansion_figure, slowdown_figure, contraction_figure, recovery_figure, cols = 2)

'''
Name: Phase Identification with Macroeconomic Conditions
Author: Jinkai Zhang
Date: August 3rd, 2020

'''

setwd("GitHub/Identification-of-business-cycles")

library(ggplot2)

us_macro = read.csv('output_macro_csv/US_macro.csv')

us_gdp_plot = 
  
  ggplot(us_macro, aes(as.Date(Date, format = "%Y-%m-%d"), APRGDP, shape
                                     = phase_GDP, colour = phase_GDP)) + 
  geom_point() +
  labs(title = "GDP Growth Classification in U.S. Stock Market (1994-2020)",
       subtitle = "High GDP Threshold = 3.41%; Low GDP Threshod = 2.01%") +
  scale_x_date(date_breaks = "3 year",
               date_labels = "%m-%Y") +
  labs(x = "Month", y = "Annulised Real GDP(%)") +
  theme_bw() +
  scale_color_manual(values = c("High" = "blue", "Stable" = "black", "Low" = "red")) +
  geom_hline(yintercept= min(subset(us_macro, phase_GDP == "High")$APRGDP), color = "orange", size = 1) +
  geom_hline(yintercept= min(subset(us_macro, phase_GDP == "Stable")$APRGDP), color = "grey", size = 1) +
  theme(

    plot.subtitle = element_text(color = "blue"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )


ggsave("output_macro_jpg//us_gdp_plot.png")

us_inflation_plot = 
  
  ggplot(us_macro, aes(as.Date(Date, format = "%Y-%m-%d"), APINFLATION, shape
                       = phase_INFLATION, colour = phase_INFLATION)) + 
  geom_point() +
  labs(title = "Inflation Classification in U.S. Stock Market (1994-2020)",
       subtitle = "High Inflation Threshold = 3.04%; Low Inflation Threshod = 1.48%") +
  scale_x_date(date_breaks = "3 year",
               date_labels = "%m-%Y") +
  labs(x = "Month", y = "Annulised Inflation(%)") +
  theme_bw() +
  scale_color_manual(values = c("High" = "blue", "Stable" = "black", "Low" = "red")) +
  geom_hline(yintercept= min(subset(us_macro, phase_INFLATION == "High")$APINFLATION), color = "orange", size = 1) +
  geom_hline(yintercept= min(subset(us_macro, phase_INFLATION == "Stable")$APINFLATION), color = "grey", size = 1) +
  theme(
    
    plot.subtitle = element_text(color = "blue"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )


ggsave("output_macro_jpg//us_inflation_plot.png")

setwd("GitHub/Identification-of-business-cycles")
backtest_us = read.csv("output_csv/Backtest_US.csv")

backtest_us_plot = 
  
  ggplot(backtest_us, aes(as.Date(Date, format = "%d/%m/%Y"), Mean) + 

  #labs(#title = "GDP Growth Classification in U.S. Stock Market (1994-2020)",
  #  subtitle = "High GDP Threshold = 3.41%; Low GDP Threshod = 2.01%") +
  scale_x_date(date_breaks = "3 year",
               date_labels = "%m-%Y") +
  labs(x = "Month", y = "Annulised Real GDP Growth Rate(%)") +
  theme_bw() +
  theme(
    
    plot.subtitle = element_text(color = "blue"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  ) +
  theme(legend.position="bottom")
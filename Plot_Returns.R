'''
Name:Plot the estimated returns based on different phases
Author: Jinkai Zhang
Date: July 21, 2020

'''
setwd("GitHub/Identification-of-business-cycles")

library(ggplot2)

return_us = read.csv('output_csv/visualization_return_us.csv')

#plot RS method
rs_us = subset(return_us, substring(return_us$Method, 1, 2) == 'RS')

Name_Reform_rs = function(x){
  for (i in 1:length(x[,1])){
    x$Method[i] = substring(x$Method[i], 17,25)
  }
  x$Mean = x$Mean * 100
  return (x)
}

rs_us = Name_Reform_rs(rs_us)

rs_us_return = 
  ggplot(rs_us, aes(fill = Phase, y = Mean, x = Method)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "Estimated Returns in Different Phases Using Regime-Switching Approch") +
  xlab("Number of Phases in Total") +
  ylab("Mean of Annualized Return (%)") +
  scale_y_continuous(limits = c(0, max(rs_us$Mean)), breaks = c(0:max(rs_us$Mean))) +
  scale_fill_manual("Phases", values = c("phase 1" = "yellow", "phase 2" = "blue", "phase 3" = "orange",
                                         "phase 5" = "black")) +
  theme_bw()

ggsave("output_jpg/visualization_methods_us//rs_us_return.png")

#plot Single Z-Score Method
zscore_us = subset(return_us, substring(return_us$Method, 1, 6) == 'Signal')

Name_Reform_zscore = function(x){
  for (i in 1:length(x[,1])){
    x$Method[i] = substring(x$Method[i], 20,28)
  }
  x$Mean = x$Mean * 100
  return (x)
}

zscore_us = Name_Reform_zscore(zscore_us)


zscore_us_return = 
  ggplot(zscore_us, aes(fill = Phase, y = Mean, x = Method)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "Estimated Returns in Different Phases Using Z-Score Transforms of Signal") +
  xlab("Number of Phases in Total") +
  ylab("Mean of Annualized Return (%)") +
  scale_y_continuous(limits = c(min(zscore_us$Mean), max(zscore_us$Mean)), breaks=c(0:max(zscore_us$Mean))) +
  scale_fill_manual("Phases", values = c("contraction" = "yellow", "expansion" = "blue", "re-acceleration" = "orange",
                                         "recovery" = "black", "slowdown" = "green")) +
  theme_bw()

ggsave("output_jpg/visualization_methods_us//zscore_us_return.png")

# Wavelet method
wave_us = subset(return_us, substring(return_us$Method, 1, 4) == 'Wave')

Name_Reform_wave = function(x){
  for (i in 1:length(x[,1])){
    x$Method[i] = substring(x$Method[i], 16,24)
  }
  x$Mean = x$Mean * 100
  return (x)
}

wave_us = Name_Reform_wave(wave_us)


wave_us_return = 
  ggplot(wave_us, aes(fill = Phase, y = Mean, x = Method)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "Estimated Returns in Different Phases Using Wavelest Transform Approach") +
  xlab("Number of Phases in Total") +
  ylab("Mean of Annualized Return (%)") +
  scale_y_continuous(limits = c(0, max(wave_us$Mean)), 
                     breaks=c(0:max(wave_us$Mean))) +
  scale_fill_manual("Phases", values = c("contraction" = "red", "expansion" = "blue", "slowdown" = "green")) +
  theme_bw()

ggsave("output_jpg/visualization_methods_us//wave_us_return.png")

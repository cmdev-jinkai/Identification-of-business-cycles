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
  #labs(#title = "GDP Growth Classification in U.S. Stock Market (1994-2020)",
  #  subtitle = "High GDP Threshold = 3.41%; Low GDP Threshod = 2.01%") +
  scale_x_date(date_breaks = "3 year",
               date_labels = "%m-%Y") +
  labs(x = "Month", y = "Annulised Real GDP Growth Rate(%)") +
  theme_bw() +
  scale_color_manual(values = c("High" = "blue", "Stable" = "black", "Low" = "red")) +
  geom_hline(yintercept= min(subset(us_macro, phase_GDP == "High")$APRGDP), color = "grey", size = 1) +
  geom_hline(yintercept= min(subset(us_macro, phase_GDP == "Stable")$APRGDP), color = "grey", size = 1) +
  theme(

    plot.subtitle = element_text(color = "blue"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5), panel.grid.major = element_blank(),panel.grid.minor = element_blank()
  ) +
  theme(axis.text=element_text(size=12), axis.title=element_text(size=12)) +
  theme(legend.text=element_text(size=12)) +
  theme(legend.position="bottom")


ggsave("output_macro_jpg//us_gdp_plot.png")

us_inflation_plot = 
  
  ggplot(us_macro, aes(as.Date(Date, format = "%Y-%m-%d"), APINFLATION, shape
                       = phase_INFLATION, colour = phase_INFLATION)) + 
  geom_point() +
  #labs(#title = "Inflation Classification in U.S. Stock Market (1994-2020)",
  #     subtitle = "High Inflation Threshold = 3.04%; Low Inflation Threshod = 1.48%") +
  scale_x_date(date_breaks = "3 year",
               date_labels = "%m-%Y") +
  labs(x = "Month", y = "Annulised Inflation Ratio (%)") +
  theme_bw() +
  scale_color_manual(values = c("High" = "blue", "Stable" = "black", "Low" = "red")) +
  geom_hline(yintercept= min(subset(us_macro, phase_INFLATION == "High")$APINFLATION), color = "grey", size = 1) +
  geom_hline(yintercept= min(subset(us_macro, phase_INFLATION == "Stable")$APINFLATION), color = "grey", size = 1) +
  theme(
    
    plot.subtitle = element_text(color = "blue"),
  ) +
  theme(
    plot.subtitle = element_text(hjust = 0.5)
  )+
  theme(axis.text=element_text(size=12), axis.title=element_text(size=12)) +
  theme(legend.text=element_text(size=12)) +
  theme(legend.position="bottom", panel.grid.major = element_blank(),panel.grid.minor = element_blank())



ggsave("output_macro_jpg//us_inflation_plot.png")


#univariate comparison
uni_all = read.csv('output_macro_csv/result_one_year.csv')

Reform_Table = function(x){
  Sharp.Ratio_GDP = x$Mean_GDP / x$Standard.Deviation_GDP
  Sharp.Ratio_GDP_Inflation = x$Mean_INFLATION / x$Standard.Deviation_INFLATION
  x = data.frame(x, Sharp.Ratio_GDP = Sharp.Ratio_GDP, Sharp.Ratio_GDP_Inflation = Sharp.Ratio_GDP_Inflation)
  return(x)
}

uni_all = Reform_Table(uni_all)

uni_us = subset(uni_all, uni_all$Country == 'US')
uni_uk = subset(uni_all, uni_all$Country == 'UK')
uni_MEXICO = subset(uni_all, uni_all$Country == 'MEXICO')
uni_BRAZIL = subset(uni_all, uni_all$Country == 'BRAZIL')

write.csv(uni_us, 'output_macro_csv//uni_us.csv')
write.csv(uni_uk, 'output_macro_csv//uni_uk.csv')
write.csv(uni_MEXICO, 'output_macro_csv//uni_MEXICO.csv')
write.csv(uni_BRAZIL, 'output_macro_csv//uni_BRAZIL.csv')


uni_us = read.csv('output_macro_csv//uni_us.csv')
uni_uk = read.csv('output_macro_csv//uni_uk.csv')
uni_MEXICO = read.csv('output_macro_csv//uni_MEXICO.csv')
uni_BRAZIL = read.csv('output_macro_csv//uni_BRAZIL.csv')


uni_us_gdp = 
  ggplot(uni_us, aes(fill = Value, y = GDP, x = phase_gdp)) + 
  geom_bar(position="dodge", stat="identity") +
  #labs(title = "One Year's Estimated Returns (US) Based on GDP Phases (1994-2020)") +
  xlab("GDP") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()+
  theme(legend.position="bottom")

ggsave("output_macro_jpg/uni_us_gdp.png")

uni_us_inflation = 
  ggplot(uni_us, aes(fill = Value, y = Inflation, x = phase_inflation)) + 
  geom_bar(position="dodge", stat="identity") +
  #labs(title = "One Year's Estimated Returns (US) Based on Inflation Phases (1994-2020)") +
  xlab("Inflation") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()+
  theme(legend.position="bottom")


ggsave("output_macro_jpg/uni_us_inflation.png")


uni_uk_gdp = 
  ggplot(uni_uk, aes(fill = Value, y = GDP, x = phase_gdp)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "One Year's Estimated Returns (UK) Based on GDP Phases (1994-2020)") +
  xlab("GDP") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()+
  theme(legend.position="bottom")

ggsave("output_macro_jpg/uni_uk_gdp.png")
order_uk = c("Below  -2.0%", "-2.0% to 0.3%", "0.3% to 2.0%", "2.0% to 3.3%",
             "3.3% to 4.4%", "4.4% to 6.1%", "Above 6.1%")
uni_uk_inflation = 
  ggplot(uni_uk, aes(fill = Value, y = Inflation, x = factor(phase_inflation, level = order_uk))) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "One Year's Estimated Returns (UK) Based on Inflation Phases (1994-2020)") +
  xlab("Inflation") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()


ggsave("output_macro_jpg/uni_uk_inflation.png")


uni_BRAZIL_gdp = 
  ggplot(uni_BRAZIL, aes(fill = Value, y = GDP, x = factor(phase_gdp, level = order_brazil))) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "One Year's Estimated Returns (Brazil) Based on GDP Phases (2000-2020)") +
  xlab("GDP") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()
ggsave("output_macro_jpg/uni_brazil_gdp.png")

uni_BRAZIL_inflation = 
  ggplot(uni_BRAZIL, aes(fill = Value, y = Inflation, x = phase_inflation)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "One Year's Estimated Returns (Brazil) Based on Inflation Phases (2000-2020)") +
  xlab("Inflation") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()



ggsave("output_macro_jpg/uni_brazil_inflation.png")

uni_MEXICO_gdp = 
  ggplot(uni_MEXICO, aes(fill = Value, y = GDP, x = phase_gdp)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "One Year's Estimated Returns (Mexico) Based on GDP Phases (1997-2020)") +
  xlab("GDP") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()

ggsave("output_macro_jpg/uni_MEXICO_gdp.png")

uni_MEXICO_inflation = 
  ggplot(uni_MEXICO, aes(fill = Value, y = Inflation, x = phase_inflation)) + 
  geom_bar(position="dodge", stat="identity") +
  labs(title = "One Year's Estimated Returns (Mexico) Based on Inflation Phases (1997-2020)") +
  xlab("Inflation") +
  ylab("Annualised Return and Sharp Ratio (%)") +
  scale_fill_manual("Value", values = c("Mean" = "blue", "Sharp.Ratio" = "Red")) +
  theme_bw()

ggsave("output_macro_jpg/uni_MEXICO_inflation.png")

us_3d = read.csv("3D_us.csv")
install.packages("plot3D")
library(plot3D)


ggplot(us_3d, aes(factor(Return), fill=factor(GDP))) + geom_bar() + facet_grid(GDP~Inflation) 

library(rgl)
library(barplot3d)

## Plot with many labels
barplot3d(rows=3,cols=3,z=us_3d$Return,theta=30,phi=50,topcolors=rainbow(6),sidecolors=rainbow(6),
          xlabels = c("First","Second","Third"),ylabels=c("Front","Back","High"),
          xsub="GDP",ysub="Inflation",zsub="Return")

us_back = read.csv('output_macro_csv/BackTest_US.csv', header = T)
class(us_back$Mean)

coeff <- 1
ggplot(us_back, aes(x=Date)) +
  theme_bw()+
  geom_line( aes(y=Mean, group = 1), color = "blue") + 
  geom_line( aes(y=Sharp.Ratio/4, group = 1), color = "Red") +
  scale_y_continuous(
  
  # Features of the first axis
  # Add a second axis and specify its features
  sec.axis = sec_axis(~.*4, name="Second Axis")
)


us_macro = read.csv('output_macro_csv/US_macro.csv')


phase_id = function(x){
  id = c()
  Phase = c()
  for (i in 1:length(x[,1])) {
    if (x$phase[i] == "LowLow") {
      Phase[i] = "LowGDP&LowInflation(1)"
      id[i] = 1
    } else if (x$phase[i] == "LowStable"){
      Phase[i]= "LowGDP&StableInflation(2)"
      id[i] = 2
    }else if (x$phase[i] == "LowHigh"){
      Phase[i] = "LowGDP&HighInflation(3)"
      id[i] = 3
    }else if (x$phase[i] == "StableLow"){
      Phase[i] = "StableGDP&LowInflation(4)"
      id[i] = 4
    }else if (x$phase[i] == "StableStable"){
      Phase[i] = "StableGDPStableInflation(5)"
      id[i] = 5
    }else if (x$phase[i] == "StableHigh"){
      Phase[i] = "StableGDP&HighInflation(6)"
      id[i] = 6
    }else if (x$phase[i] == "HighLow"){
      Phase[i] = "HighGDP&LowInflation(7)"
      id[i] = 7
    }else if (x$phase[i] == "HighStable"){
      Phase[i] = "HighGDP&StableInflation(8)"
      id[i] = 8
    }else if (x$phase[i] == "HighHigh"){
      Phase[i] = "HighGDP&HighInflation(9)"
      id[i] = 9
    }
  }
  x = data.frame(x, phase_id = id, Phase = Phase)
  return(x)
}

write.csv(us_macro_id,'us_macro_id.csv')

us_macro_id = phase_id(us_macro)

Macro_GDP_id = 
  ggplot(us_macro_id, aes(as.Date(Date, format = "%Y-%m-%d"), as.numeric(phase_id), colour = Phase)) + 
  geom_line(aes(group = 1)) +
  #labs(title = "Phase Identification in Nine Regimes using Macroeconomic Conditions (1993-2020)") +
  scale_x_date(labels = date_format("%m-%Y")) + 
  labs(x = "Month", y = "") +
  theme_bw() +
  #ylim(0,9) +
  scale_y_continuous( breaks =0:9)+
  theme(legend.position="bottom", panel.grid.major = element_blank(),panel.grid.minor = element_blank())#  +
  scale_color_manual(values = c("LowGDP&LowInflation" = "yellow", "LowGDP&StableInflation" = "grey39",
                                "LowGDP&HighInflation" = "black", "StableGDP&LowInflation" = "orange2",
                                "StableGDP&StableInflation" = "red","StableGDP&HighInflation" = "red4",
                                "HighGDP&LowInflation" = "pink", "HighGDP&StableInflation" = "green",
                                "HighGDP&LowInflation" = "blue" ))





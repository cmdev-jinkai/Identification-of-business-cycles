'''
Name:Plot the Dynamic bubble chart with panel data for different countries
Author: Jinkai Zhang
Date: July 22, 2020

'''
setwd("GitHub/Identification-of-business-cycles")

library(gapminder)
library(ggplot2)
library(gganimate)
library(gifski)

returns_panel = read.csv('output_csv/returns_panel.csv')

returns_panel = data.frame(returns_panel, Sharp.Ratio = returns_panel$Mean / returns_panel$Standard.Deviation)
returns_panel = subset(returns_panel, returns_panel$Year >= 1 & returns_panel$Year <= 7  )


dynamic_bubble = 
  ggplot(returns_panel, aes(Standard.Deviation, Mean, size = Sharp.Ratio, color = Country)) +
  geom_point() +
  #scale_x_log10() +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(2, 20)) +
  theme_bw() +
  labs(title = 'Year: {frame_time}', x = 'Standard Deviation (%)',  y = 'Mean of Annualized Return (%)',
       subtitle = "Estimated Returns Based on the Latest Phase from Seven Countries") +
  transition_time(Year) +
  ease_aes('linear')

setwd("output_jpg//visualization_dynamic_bubble")

animate(dynamic_bubble, duration = 10, fps = 20,  renderer = gifski_renderer())
anim_save( "dynamic_bubble.gif")

returns_panel_add = subset(returns_panel, returns_panel$Year == 3)

figure_add =   
  
  ggplot(returns_panel_add, aes(y = Mean, x = Standard.Deviation)) + 
  geom_point(aes(color = Country,  size = Sharp.Ratio), alpha = 2) +
  labs( title = "Latest M/T Return Estimate over 3-Years Horizon") +
  ylab("Nonimal Annualized Return (%)") +
  xlab("Annulised Volatility (%)") +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(5, 15)) +
  theme_bw() +
  theme(
    plot.title = element_text(color = "black", size = 12,face = "bold"),
    plot.subtitle = element_text(color = "blue", face = "bold"),
  ) +
  theme(legend.position="bottom")+
  theme(
    plot.title = element_text(hjust = 0.5)
  ) 


write.csv(returns_panel_add, "Estimation_Latest.csv")







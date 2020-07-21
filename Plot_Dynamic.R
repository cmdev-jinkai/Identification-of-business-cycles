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
returns_panel = subset(returns_panel, returns_panel$Year >= 2)


dynamic_bubble = 
  ggplot(returns_panel, aes(Mean, Standard.Deviation, size = Sharp.Ratio, color = Country)) +
  geom_point() +
  #scale_x_log10() +
  scale_color_manual(values = c("BRAZIL" = "yellow", "FRANCE" = "pink", "GERMANY" = "orange",
                                "JAPAN" = "black", "MEXICO" = "green", "UK" = "blue", "US" = "red")) +
  scale_size(range = c(2, 20)) +
  theme_bw() +
  labs(title = 'Year: {frame_time}', x = 'Mean of Annualized Return (%)', y = 'Standard Deviation (%)',
       subtitle = "Estimated Returns Based on the Latest Phase from Seven Countries") +
  transition_time(Year) +
  ease_aes('linear')

setwd("output_jpg//visualization_dynamic_bubble")

animate(dynamic_bubble, duration = 10, fps = 20,  renderer = gifski_renderer())
anim_save( "dynamic_bubble.gif")

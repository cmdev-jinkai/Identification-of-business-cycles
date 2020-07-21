'''
Name:Plot the  bubble chart for different countries
Author: Jinkai Zhang
Date: July 21, 2020

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

# plot bubble chart in different regimes using 4 phases in single based input

return_phase_four = subset(return_all, Method == 'Signal based (incl. 4 phases)') 

return_phase_expansion = subset(return_phase_four, Phase == 'expansion')
return_phase_contraction = subset(return_phase_four, Phase == 'contraction')
return_phase_recovery = subset(return_phase_four, Phase == 'recovery')
return_phase_slowdown = subset(return_phase_four, Phase == 'slowdown')


expansion_figure =
  ggplot(return_phase_expansion, aes(x = Mean, y = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Expansion Phase") +
  xlab("Mean of Annualized Return (%)") +
  ylab("Standard Deviation (%)") +
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
  ggplot(return_phase_slowdown, aes(x = Mean, y = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Slowdown Phase") +
  xlab("Mean of Annualized Return (%)") +
  ylab("Standard Deviation (%)") +
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
  ggplot(return_phase_contraction, aes(x = Mean, y = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Contraction Phase") +
  xlab("Mean of Annualized Return (%)") +
  ylab("Standard Deviation (%)") +
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
  ggplot(return_phase_recovery, aes(x = Mean, y = Standard.Deviation)) + 
  geom_point(aes(color = Country, size = Sharp.Ratio), alpha = 0.5) +
  labs(title = "Annualised Return Estimation in Four Phases",
       subtitle = "Recovery Phase") +
  xlab("Mean of Annualized Return (%)") +
  ylab("Standard Deviation (%)") +
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


all_phase_figure =
  multiplot(expansion_figure, slowdown_figure, contraction_figure, recovery_figure, cols = 2)



# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
# reference: http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_(ggplot2)/
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}










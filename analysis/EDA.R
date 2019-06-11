library(data.table)
library(ggplot2)
library(cowplot)

wd <- 'C:\\Users\\willf\\Documents\\Data 515\\Project'

setwd(wd)

data.2015 <- fread('marathon_results_2015.csv', stringsAsFactors = FALSE)

data.2015[, Pace := as.integer(as.ITime(Pace))]
data.2015[, time_5K := as.integer(as.ITime(`5K`))]
data.2015[, time_10K := as.integer(as.ITime(`10K`))]
data.2015[, time_20K := as.integer(as.ITime(`20K`))]
data.2015[, time_30K := as.integer(as.ITime(`30K`))]
data.2015[, time_40K := as.integer(as.ITime(`40K`))]
data.2015[, Country := factor(ifelse(Country == 'USA', 'USA', 'Else'))]
data.2015[, Gender := factor(`M/F`)]
data.2015[, Age := factor(Age)]
data.2015 <- data.2015[complete.cases(data.2015[, .(Age, Gender, Country, time_5K, time_10K, time_20K, time_30K, time_40K, Pace)])]

plot_model_marathon <- function(data, formula, x_axis) {
  data <- copy(data)
  
  model.2015 <- glm(data = data, formula = formula, family = poisson)
  data[, fitted := model.2015[['fitted.values']]]
  response <- as.character(formula[2])
  
  data.2015.agg <- data[
    , .(
      obs = mean(get(response), na.rm = TRUE)
      , fitted = mean(fitted, na.rm = TRUE)
      , counts = .N
    ), keyby = x_axis
  ]
  
  data.2015.melt <- melt(
    data.2015.agg
    , id.vars = x_axis
    , measure.vars = c('obs', 'fitted')
    , value.name = response
    , variable.name = 'Type'
  )
  
  p.volume <- ggplot(data.2015.agg, aes_string(x_axis, 'counts')) + geom_bar(stat = 'identity') + theme_void()
  
  p.a2e <- ggplot(
    data.2015.melt
    , aes_string(x = x_axis, y = response, color = 'Type', group = 'Type')
  ) + geom_line() + theme_bw()
  
  plot_grid(p.volume, p.a2e, nrow = 2, rel_heights = c(0.15, 0.85), align = 'v')
}

plot_model_marathon(data = data.2015, formula = as.formula('time_40K ~ Age + I(Age^2) + Gender + time_5K'), x_axis = 'Age')
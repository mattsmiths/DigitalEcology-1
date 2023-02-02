#load data from file
filename <- '/Users/jamescrall/Documents/GitHub/DigitalEcology/MiniProject1/examples/TemperatureLogger/inside_logger.csv'
  #NB This filename will be specific to your computer and will need to be modified.
  # On mac, a shortcut to finding full pathnames is to control click (or right click), 
  # and then press 'option', and click 'Copy 'your file' as Pathname'
  #
  # On Windows, you can do the same by pressing the Shift Key and right-clicking, then 'Copy as Path'

temp_data <- read.csv(filename)
  #Reads csv from file directly into a data frame

colnames(temp_data) <- c('time', 'pressure', 'temp', 'humidity')
  #Manually add column names

head(temp_data)
  #Very useful function that shows you the 

library(lubridate)
  #

start.date <- parse_date_time('2022-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
  #Create a reference time point to calculate differences relative to


data$datenum <- as.numeric(difftime(parse_date_time(data$time, 'ymd-HMS'),start.date))

plot(temp~datenum, data = data, pch = 19, col = "blue", axes = FALSE)
axis(1)
axis(2)
by_tailnum <- flights %>%
  filter(dep_delay>0, month==12, origin == 'EWR') %>% 
  group_by(tailnum, carrier)
delay <- summarise(by_tailnum, 
                   delay = mean(dep_delay, na.rm = TRUE))

ggplot(delay, aes(carrier, delay)) + 
  geom_boxplot() +
  scale_y_continuous(limits=c(0,200)) +
  labs(title = "Retrasos de diciembre en Newark de las distintas compañias", x = "Compañia", y = "Retraso(mins.)")

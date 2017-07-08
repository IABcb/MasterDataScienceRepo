by_tailnum <- flights %>%
  filter(arr_delay>0) %>% 
  mutate(mes = month.abb[month]) %>% 
  group_by(tailnum, mes)
delay <- summarise(by_tailnum, 
                   count = n(), 
                   dist = mean(distance, na.rm = TRUE),
                   delay = mean(arr_delay, na.rm = TRUE))
delay$mes<- factor(delay$mes,month.abb)

ggplot(delay, aes(dist, delay)) +
  geom_point(aes(size = count), alpha = 1/2) +
  xlim(c(0,2500)) + 
  ylim(c(0,400)) +
  labs(title="Relación entre distancia de los vuelos y retrasos en su llegada", x="Distancia (millas)", y="Retraso (mins.)") +
  geom_smooth(method = 'gam') +
  scale_size_area() +
  scale_radius(name="Núm. vuelos") + 
  facet_wrap(~mes, ncol = 3)
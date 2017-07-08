by_tailnum <- flights %>%
  filter(dep_delay>0, distance<1000, origin == 'JFK') %>% 
  mutate(mes = month.abb[month]) %>% 
  group_by(tailnum, mes)
delay <- summarise(by_tailnum, 
                   count = n(), 
                   dist = mean(distance, na.rm = TRUE),
                   delay = mean(dep_delay, na.rm = TRUE))
delay$mes<- factor(delay$mes,month.abb)

ggplot(delay, aes(dist, delay)) +
  geom_point(aes(size = count), alpha = 1/2) +
  xlim(c(0,1000)) + 
  ylim(c(0,250)) +
  labs(title="Relación entre distancia de los vuelos de JFK y retrasos en su salida", x="Distancia (millas)", y="Retraso (mins.)") +
  geom_smooth(method = 'gam') +
  scale_size_area() +
  scale_radius(name="Núm. vuelos") + 
  facet_wrap(~mes, ncol = 3)
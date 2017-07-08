library(ggplot2)
library(dplyr)
library(nycflights13)

## Cuantos vuelos se realizan cada mes
flights %>%
  group_by(month) %>%
  summarise(vuelos = n())
  
## Que aeropuerto tiene el mayor numero de salidas
flights %>%
  group_by(origin) %>%
  summarise(salidas = n()) %>%
  top_n(1)

## Compañia con mayor numero de salidas en verano
flights %>%
  filter(month==c(6,7,8,9)) %>%
  group_by(carrier) %>%
  summarise(verano = n()) %>%
  top_n(1)

## Compañia con mayor tiempo de vuelo en todo el año
flights %>%
  group_by(carrier) %>%
  summarise(tiempo = sum(air_time,na.rm=TRUE)) %>%
  top_n(1)

## Compañia con mayor retraso en la salida de los vuelos
flights %>%
  group_by(carrier) %>%
  summarise(tiempo = sum(dep_delay,na.rm=TRUE)) %>%
  top_n(1)

## Tiene alguna correlacion los retrasos con la duracion
by_tailnum <- group_by(flights, tailnum)
delay <- summarise(by_tailnum,
                   count = n(),
                   dist = mean(distance, na.rm = TRUE),
                   delay = mean(dep_delay, na.rm = TRUE))

ggplot(delay, aes(dist, delay)) +
  geom_point(aes(size = count), alpha = 1/2) +
  labs(x="Distancia (millas)", y="Retraso (mins.)") +
  xlim(c(0,2500)) + 
  ylim(c(-20,75)) +
  geom_smooth(method = 'gam') +
  scale_size_area() +
  ggtitle("Relacion entre distancia y retrasos en los vuelos") +
  scale_radius(name="Num. vuelos")


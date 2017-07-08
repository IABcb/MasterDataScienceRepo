load("DatosEncuestaUSA.RData")

hijos<-Y$CHILDS[Y$FEMALE==1 & Y$YEAR>=1990 & Y$AGE==40 & !is.na(Y$DEG)]
hijos<-hijos[!is.na(hijos)]

med <- mean(hijos) #Media de la muestra

p.seq=seq(0,3,length=1000)
plot(p.seq,dgamma(p.seq,2,1),type="l",xlab="p",ylab="densidad",ylim=c(0,4)) #Gamma(2,1)
lines(p.seq,dgamma(p.seq,285,156),col=2,xlab="p",ylab="densidad") #Gamma(285,156)

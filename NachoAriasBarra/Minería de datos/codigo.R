# LIBRERIAS
library(dplyr)
library(ggplot2)
library(lattice)
library(reshape2)
library(caret)
library(mlbench)
library(rpart)
library(party)
library(ROCR)
library(forcats)
library(corrplot)
library(DMwR2)
library(class)
library(mice)
library(e1071)
library(lattice)
library(DMwR2)
library(foreach)
library(class)
library(devtools)
library(randomForest)
library(adabag)
library(plotrix)
library(neuralnet)
rm(list=ls())
set.seed(39)




# FUNCIONES

# En la sección de funciones se desarollarán aquellas necesarias para conseguir un 
# código más manejable y legible en la parte del análisis de los datos.

### PREPARACION DE LOS DATOS

##### Limpieza de datos

removeLitoNA <- function(data){
  # Filtramos por los valores nulos de la variable respuesta
  data <- data %>% filter(!is.na(Lito))
}

cleandata <- function(data){
  # Los valores -999.250 no tienen sentido
  data[data == -999.25] = NA
  
  
  # Agrupamos la variable respuesta en 3 grupos, ya que de estos dos grupos hay muy pocos casos
  data[which(data$Lito == 'Carb shale'),'Lito'] <- 'Shale'
  data[which(data$Lito == 'Sandstones'),'Lito'] <- 'Shale'
  data$Lito <- droplevels(data$Lito)
  
  # Quitamos la variable profundidad, por relacion practicamente 1 a 1 con la salida
  data <- data[,-2]
  n_col <- ncol(data)
  
  return(list(clean_data = data,n_col = n_col))
} 


##### Visualización de histogramas

var_histograms <- function(data){
  d <- melt(data)
  ggplot(d,aes(x = value, fill = Lito)) + 
    facet_wrap(~variable,scales = "free_x") + 
    geom_histogram()
}

##### Visualización de correlaciones

corrplot_func <- function(cor){
  corrplot(cor,type="upper",tl.pos="d",tl.cex=0.75)
  corrplot(cor,add=TRUE, type="lower", method="number", diag=FALSE,tl.pos="n", cl.pos="n")
}

##### Estimación de los datos faltantes o NAs
  
###### Knn

imput_data_knn <- function(data, knn_factor, nORp=0.2, method = 'median'){
  data <- data[-manyNAs(data, nORp = nORp),]
  data <- knnImputation(data, k = knn_factor, meth = method)
  return(data)
}


### MUESTREO

##### Train y Test


# Split datasets in train and test
splitdata_test_train <- function (data_df, train_percentage){
  
  n_data=dim(data_df)[1]
  
  n_train=round(train_percentage*n_data)
  # Tomamos el resto para test
  n_test=n_data-n_train
  
  # Creamos los indices del conjunto de entrenamiento y de test, 
  # ya que los hemos cogido aleatoriamente
  indices=1:n_data
  # Cogemos una muestra de los indices de n_train
  indices_train= sample(indices,n_train)
  # Aqui coge los indices contrarios
  indices_test=indices[-indices_train]
  # La idea es quedarnos con las filas de cada tipo de dato, no con los datos
  
  data_df_train=data_df[indices_train,]
  data_df_test=data_df[indices_test,]
  
  return(list(training = data_df_train, test = data_df_test))
  
  # La salida es:
  # output <- splitdata_test_train(data_df, train_percentage)
  # output$training
  # output$test
}

##### Medición del rendimiento de clasificación

mediciones <- function(cm){
  accuracy <- sum(diag(cm))/sum(cm)
  precision <- diag(cm)/rowSums(cm)
  recall <- (diag(cm)/colSums(cm))
  print("Accuracy")
  print(accuracy)
  print("Precision")
  print(precision)
  print("Recall")
  print(recall)
  return(data.frame(acc=accuracy,prec=precision,rec=recall))
}

### MODELADO

##### Arbol decisión

##### Random Forest

myRandomForest <- function(data_df, col_in, col_ans, data_train_df, data_test_df, n_trees = 100, n_vars_tree = 4, n_samples_tree = 100, data_split = 'gini'){
  # Pasos del proceso:
  # 1. Dividimos el conjunto en train y test
  # 2. Creación del bosque
  
  ## N n_trees --> numero de arboles
  ## K n_vars_tree --> numero de variables en cada arbol
  ## M n_samples_tree --> numero de muestras en cada arbol
  ## data_df --> datos en un dataframe
  ## col_in --> columnas del modelo
  ## col_ans --> columna respuesta, deben ser factores
  ## data_train_df --> conjunto de training
  ## data_test_df --> conjunto de test
  ## data_split --> método de split de los datos del bosque
  
  # 3. Error en train --> votaciones de los arboles. Se calcula el que más veces se ha votado
  # 4. Error en test --> votaciones de los arboles. Se calcula el que más veces se ha votado
  
  x.train=  data_train_df
  x.test = data_test_df
  
  # Lista de árboles (modelos)
  models= vector("list", n_trees) 
  # Guardamos el número de cada variable usada en cada modelo o árbol. Inicializamos esa matriz
  vars=matrix(0,n_vars_tree,n_trees)
  
  # Tamanno de la muestra de train
  k=dim(x.train)[1] 
  # Para cada árbol...
  for (i in 1:n_trees) 
  {
    # a son los indices de las variables de cada modelo, de las n_vars_tree posibles, ordenadas
    a=sort(sample(col_in,n_vars_tree))
    # b son los indices de los n_samples_tree individuos para cada arbol
    b=sort(sample(1:k,n_samples_tree,replace=TRUE))
    # Matriz de b indices de individuos (filas) por a columnas, # que son las variables mas la respuesta, la 14
    x.train.vot=x.train[b,c(a,col_ans)]
    
    model.rp <- rpart(x.train.vot[,n_vars_tree+1] ~., data=x.train.vot[,1:n_vars_tree], cp=0.0001, parms=list(split=data_split))
    # Guardamos el modelo
    models[[i]]=model.rp 
    # Guardamos las variables
    vars[,i]=as.vector(a) 
  }
  
  # ERROR EN TRAIN
  # Filas como individuos y columnas cada una de las votaciones de cada arbol
  y.old.predict.matrix=matrix(0,k,n_trees) 
  # Rellenamos por columna. Sacamos un modelo y
  # damos las predicciones para cada individuo 
  # para ese modelo, es decir, la columna.
  for (j in 1:n_trees) 
  {
    # Sacamos la columna de predicciones del primer modelo, para todos los indiviuos y guardamos las variables de vars
    prediction=predict(models[[j]], x.train[,vars[,j]]) 
    # Pasamos a factores
    factores=colnames(prediction) 
    prediction.fact= factores[max.col(prediction)]
    # Metemos las votaciones en la columna del modelo para todos los individuos
    y.old.predict.matrix[,j]= prediction.fact 
  }
  # Elegimos para cada fila el factor con mayor probabilidad (más veces aparece en la fila)
  # Revisar esto
  max_freq <- apply(y.old.predict.matrix,1,function(x) names(which.max(table(x))))
  
  y.train.pred.fact=max_freq
  y.real.train.fact=x.train[,col_ans]
  table.rforest.train=table(y.train.pred.fact,y.real.train.fact)
  
  # ERROR EN TEST
  m=dim(x.test)[1] #tamanno de la muestra de test
  y.new.predict.matrix=matrix(0,m,n_trees)
  for (j in 1:n_trees)
  {
    prediction=predict(models[[j]], x.test[,vars[,j]] )
    factores=colnames(prediction)
    prediction.fact= factores[max.col(prediction)]
    y.new.predict.matrix[,j]= prediction.fact
  }
  
  max_freq <- apply(y.new.predict.matrix,1,function(x) names(which.max(table(x))))
  
  y.test.pred.fact = max_freq
  y.real.test.fact=x.test[,col_ans]
  table.rforest.test=table(y.test.pred.fact,y.real.test.fact)
  
  return(list(forest_test = table.rforest.test, forest_train = table.rforest.train, cm = table.rforest.test))
}

###############################################################################################
#                               *PROGRAMA PRINCIPAL*  
## 2. DESCRIPCION DE LOS DATOS

#### Carga de datos

data_drill <- read.table("../../data/drill.txt", sep=",", header=TRUE)
summary(data_drill)

#### Exportación de datos sin tratar a csv

write.csv(data_drill, file = "DirtyData.csv")

#### Histograma de los datos sin tratar

var_histograms(data_drill)

## 3. PREPARACION DE LOS DATOS

#### Limpieza de datos

data_drill_no_NA_Lito <- removeLitoNA(data_drill)
data_output <- cleandata(data_drill_no_NA_Lito) 
data_drill <- data_output$clean_data
num_cols <- data_output$n_col

var_histograms(data_drill_no_NA_Lito)

#### Normalización de variables

for(name in c("RLL3","RILD","RILM","DCAL","MCAL","MI","MN","RHOC"))
{
  i <- which(colnames(data_drill)==name)
  data_drill[i] <- log(data_drill[i])
}


#### Visualización histogramas antes de las estimaciones de datos faltantes

summary(data_drill)
var_histograms(data_drill)

#### Visualización de correlaciones antes de las estimaciones de datos faltantes

cm_prev <- cor(data_drill[complete.cases(data_drill),-1])
corrplot_func(cm_prev)

##### Estimación de datos faltantes - Knn

data_drill_knn <- imput_data_knn(data_drill,4,nORp = 0.2, "median")

#### Estimación de datos faltantes - MICE

data_drill_MICE <- imput_data_multiple(data_drill, m = 5, maxit = 50, method = "pmm", seed = 300, printFlag = FALSE)

#### Visualización histogramas a posteriori de las estimaciones de datos faltantes

summary(data_drill_knn)
summary(data_drill_MICE)

var_histograms(data_drill_knn)
var_histograms(data_drill_MICE)


#### Visualización de correlaciones a posteriori de las estimaciones de datos faltantes

cm_post_knn <- cor(data_drill_knn[,-1])
corrplot_func(cm_post_knn)

#### Diferencia antes y después de las estimaciones de datos faltantes

cm_dif_knn <- cm_post_knn - cm_prev
corrplot_func(cm_dif_knn)

cm_dif_MICE <- cm_post_MICE - cm_prev
corrplot_func(cm_dif_MICE)

data_drill <- data_drill_knn

##### Train y Test

train_percentage=0.7
data_output <- splitdata_test_train(data_drill, train_percentage)
train_df <- data_output$training
summary(train_df)
test_df <- data_output$test
summary(test_df)

## 4. MODELADO

##### Regresión logística

levels(train_df[,1])
aux <- train_df
aux[,1] <- 0
aux_test <- test_df
aux_test[,1] <- 0

# Objetivo: diferenciar entre limestones y otro tipo de rocas
aux[which(train_df[,1]=="Cherty limestones"),1] <- "Limestones"
aux[which(train_df[,1]=="Limestones"),1] <- "Limestones"
aux[which(train_df[,1]=="Shale"), 1] <- "Others"
aux[which(train_df[,1]=="Anhidrite"),1] <- "Others"

aux_test[which(test_df[,1]=="Cherty limestones"),1] <- "Limestones"
aux_test[which(test_df[,1]=="Limestones"),1] <- "Limestones"
aux_test[which(test_df[,1]=="Shale"), 1] <- "Others"
aux_test[which(test_df[,1]=="Anhidrite"),1] <- "Others"


aux[,1] <- as.factor(aux[,1])
aux_test[,1] <- as.factor(aux_test[,1])

data_drill_glm = glm(Lito ~ ., family=binomial(link='logit'), data=aux)

summary(data_drill_glm)


pred <- predict(data_drill_glm,test_df)
pred <- ifelse(pred > 0.5,"Others","Limestones")
cm <- table(pred=pred,real=aux_test[,1])
print(cm)
mediciones(cm)

##### Knn

train_df_knn = train_df[,-(1), drop=FALSE]
test_df_knn = test_df[,-(1), drop=FALSE]
train_labels = train_df[,1]

knn_model = knn(train_df_knn, test_df_knn, cl=train_labels, k=3)
cm <- table(pred=knn_model,real=test_df[,1])
print(cm)

mediciones_knn <- mediciones(cm)

##### Arbol decisión

data_drill_tree <- ctree(Lito ~ ., data=train_df)
pred <- predict(data_drill_tree, test_df)
# summary(test_df[,1])

# pred <- ifelse(pred > 0.5,1,0)
cm <- table(pred=pred,real=test_df[,1])
print(cm)

# print.tree(data_drill_tree)
summary(data_drill_tree)

mediciones_dt <- mediciones(cm)

plot(data_drill_tree)

##### Random Forest

mrf <- myRandomForest(data_df = data_drill, col_in = 2:21, col_ans = 1,  data_train_df = train_df, data_test_df = test_df, n_trees = 100, n_vars_tree = 4, n_samples_tree = 1000, data_split = 'information')
print(mrf$cm)
mediciones_mrf <- mediciones(mrf$cm)


lito.rf = randomForest::randomForest(Lito ~ ., train_df)
pred <- predict(lito.rf,test_df)
print(lito.rf)
cm <- table(pred=pred,real=test_df[,1])
print(cm)
mediciones_rf2 <- mediciones(cm)


##### Bagging

bagging_model <- bagging(Lito ~ ., data=train_df, mfinal=10)
#Predicting with labeled data
predbagging_model_train <-predict.bagging(bagging_model, newdata=train_df)
predbagging_model_test <-predict.bagging(bagging_model, newdata=test_df)

cm <- predbagging_model_train$confusion
print(cm)
mediciones(cm)

cm <- predbagging_model_test$confusion
print(cm)
mediciones_prebag <-mediciones(cm)

##### Boosting

adaboost_model <- boosting(Lito~., data=train_df, boos=TRUE, mfinal=6)
predboost_model_train<-predict.boosting(adaboost_model, newdata=train_df)
predboost_model_test<-predict.boosting(adaboost_model, newdata=test_df)
predboost_model_train$confusion
predboost_model_test$confusion

cm <- predboost_model_train$confusion
print(cm)
mediciones(cm)

cm <- predboost_model_test$confusion
print(cm)
mediciones_boost <- mediciones(cm)

importanceplot(adaboost_model)

##### SVM
svm_model <- svm(x=train_df[,-1], y=train_df$Lito, type = "C-classification", kernel="radial", cost=10, gamma=.5)

svm_predictions_train = predict(svm_model, train_df[,-1])
svm_predictions_test = predict(svm_model, test_df[,-1])

cm <- table(pred=svm_predictions_train, real=train_df[,1])
print(cm)
mediciones(cm)

cm <- table(pred=svm_predictions_test,real=test_df[,1])
print(cm)
mediciones_svm <- mediciones(cm)

##### Neural network

# https://www.r-bloggers.com/multilabel-classification-with-neuralnet-package/

# Scale columns
maxs <- apply(train_df[,-1], 2, max) 
mins <- apply(train_df[,-1], 2, min)
scaled_train = as.data.frame(scale(train_df[,-1], center = mins, scale = maxs-mins))
scaled_test = as.data.frame(scale(test_df[,-1], center = mins, scale = maxs-mins))

scaled_train <- cbind(scaled_train,nnet::class.ind(as.factor(train_df$Lito)))
scaled_test <- cbind(scaled_test,nnet::class.ind(as.factor(test_df$Lito)))

names(scaled_train)[which(names(scaled_train)=="Cherty limestones")] <- "Cherty"
names(scaled_test)[which(names(scaled_test)=="Cherty limestones")] <- "Cherty"

nn <- neuralnet(Anhidrite+Cherty+Limestones+Shale~BVTX+AVTX+RxoRt+CILD+RLL3+SP+RILD+RILM+DCAL+RHOB+RHOC+DPOR+CNLS+GR+MCAL+MI+MN+DT+ITT+SPOR, 
                data=scaled_train, 
                hidden=c(3,2), 
                act.fct = "logistic",
                err.fct = "sse",
                linear.output = F,
                lifesign = "minimal",
                threshold = 0.1,
                rep = 5
)
plot(nn)
pr.nn <- compute(nn, scaled_test %>% select(-Anhidrite,-Cherty,-Limestones,-Shale))
pr.nn_ <- pr.nn$net.result

original_values <- max.col(scaled_test[, 21:24])
pr.nn_2 <- max.col(pr.nn_)
mean(pr.nn_2 == original_values)


# Evaluacion

mediciones_dt$alg <- rep("dt",4)
mediciones_knn$alg <- rep("knn",4)
mediciones_mrf$alg <- rep("mrf",4)
mediciones_rf2$alg <- rep("rf2",4)
mediciones_svm$alg <- rep("svm",4)
mediciones_boost$alg <- rep("boost",4)
# mediciones_bag$alg <- rep("bag",4)
mediciones_prebag$alg <- rep("prebag",4)
union_mediciones <- rbind(mediciones_dt,
                          mediciones_knn,
                          mediciones_mrf,
                          mediciones_rf2,
                          mediciones_svm,
                          mediciones_boost,
                          # mediciones_bag,
                          mediciones_prebag)
union_mediciones$alg <- factor(union_mediciones$alg)

union_mediciones_no_acc <- union_mediciones %>% select(-acc)

# Plot comparacion
par(bg = "burlywood1")
plot(union_mediciones_no_acc$prec, union_mediciones_no_acc$rec, 
     col=union_mediciones_no_acc$alg, 
     pch=rownames(union_mediciones_no_acc), 
     xlab = "Precision", ylab = "Recall", xlim = c(0,1), ylim=c(0,1))
draw.arc(1, 1, (sqrt(2)/2)*(1:100/10), deg2=-360, col = 1, lty=3)
legend(x="topleft", legend = unique(union_mediciones_no_acc$alg), fill=unique(union_mediciones_no_acc$alg))
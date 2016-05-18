#!/bin/bash


#ITERACIONES DE LAS PRUEBAS
ITER=$1
if [ "$1" = "" ];then
	echo "Se lanza 10 veces por defecto";
	ITER=10
fi


#NUMERO DE THREADS QUE LANZA
THREADS=2
	
FILE="/tmp/result.`date +%d.%m.%Y_%H.%M.%S`_TH$THREADS_ITER$ITER.txt"
touch $FILE

for i in $(seq 1 $ITER);do
	MASTER=spark://10.0.2.10:7077 /root/spark/bin/run-example SparkPi $THREADS | awk '{print $4}' |tee -a $FILE
done 


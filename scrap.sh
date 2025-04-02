#!/bin/bash


source *env/bin/activate


while true; do
    
    *env/bin/python main.py -a exemplo_empresas.csv 

    sleep 60

done

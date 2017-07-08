#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 18:16:22 2016

@author: usuario
"""

import csv

csvFile = open('Transporte.csv','wt')
writer = csv.writer(csvFile)

names = ['transportmean_name','line_number','order_number','stop_id','stop_code','stop_name','stop_desc','stop_lat','stop_lon','zone_id','stop_url','location_type','parent_station','stop_timezone','wheelchair_boarding']
writer.writerow(names)

reader = csv.reader(open('./Metro/Metro.csv', 'r'))
for row in enumerate(reader):
    writer.writerow(row[1])
    
reader = csv.reader(open('./Tranvia/Tranvia.csv', 'r'))
for row in enumerate(reader):
    writer.writerow(row[1])
    
reader = csv.reader(open('./Cercanias/Cercanias.csv', 'r'))
for row in enumerate(reader):
    writer.writerow(row[1])
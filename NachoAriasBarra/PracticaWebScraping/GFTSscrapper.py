#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 18:08:39 2016

@author: nacho
"""
import requests
from bs4 import BeautifulSoup
import zipfile, io
import os
import csv

def getHTML(url,user_agent):
    user = {'User-Agent': user_agent}
    try:
        html = requests.get(url,headers = user)        
    except ConnectionError as e:
        print ('Download error:', e.reason)
        html = None
    return html

def getBsObj(html):
    return BeautifulSoup(html.text, "html.parser")   
    
def getMainUrl(bsObj):
    return bsObj.find('a').attrs['href'] 

def get_download_page(p):
    return p[-1].find('a').attrs['href']
    
def is_transport(transports, p, text):
    is_trans = False
    for transport in transports:
        if p[0].find('a').attrs['title'] == text + transport:
           is_trans = True
    return is_trans
        
def get_pages_download(transports, bsObj):
    text = 'Conjunto de datos de la red de '
    pages_download = []
    div = bsObj.find("div",{"class": "custom-layout"})
    for div in div.findAll('div')[2:8]:        
        p = div.findAll('p')
        if is_transport(transports, p, text):
            pages_download.append(get_download_page(p))
    return pages_download

def get_item(item_url):
    return item_url.split('/')[-1].split('=')[-1]

def download_items(pages_download, agent, transports):
    main_url = 'http://crtm.maps.arcgis.com/sharing/rest/content/items/'
    n=0
    for page in pages_download:
        print(page)
        item = get_item(page)
        url = main_url + item + '/data'
        r = getHTML(url,agent)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        try:
            dir = transports[n].replace(' ','')
        except:
            dir = transports[n]
        os.system('mkdir ' + dir)
        os.system('chmod 777 ' + dir)
        z.extractall(dir)
        n+=1

def translate_trans(transport):
    abv=[]
    if transport == 'Metro':
        abv.append('METRO')
    elif transport == 'Cercanías':
        abv.append('CR')
    elif transport == 'MetroLigero':
        abv.append('ML')
    return abv
    
def get_csv_from_stops():

    txt_file_name = "stops.txt"
    
    csvFile = open("stops.csv", 'w', encoding= 'UTF-8')
    writer = csv.writer(csvFile, dialect="excel", lineterminator='\n')
        
    transports = ['Metro','Cercanías','MetroLigero']
    
    header = False
    insert_cols = ['','']
    for transport in transports:
        nfil=0
        file = open(transport + '/' + txt_file_name,'r')
        for line in file:
            line = line.split(',')
            if nfil > 0:
                row = translate_trans(transport)
                row += line

                writer.writerow(row)        
            else:
                if not header:
                    beginning_header = ['transportmean_name']
                    header = beginning_header + line
                    writer.writerow(header) 
                    header = True
            nfil+=1    
    csvFile.close()

        
if __name__ == "__main__": 

    # Main data
    url_opendata = 'http://datos.crtm.es'
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    transports = ['Metro', 'Metro Ligero', 'Cercanías']
    pages_download = []
    
    # We download the HTML and bsOBj
    html_pre = getHTML(url_opendata,agent)
    bsObj_pre = getBsObj(html_pre)    
    main_url = getMainUrl(bsObj_pre)
    html = getHTML(main_url,agent)
    bsObj = getBsObj(html)    
    
    # We get the download pages for a new scraping for each transport
    pages_download = get_pages_download(transports, bsObj)
    download_items(pages_download, agent, transports)

    # We merge all the data into a csv file
    get_csv_from_stops()    

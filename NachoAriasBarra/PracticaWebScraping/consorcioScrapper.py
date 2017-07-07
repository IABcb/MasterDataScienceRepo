# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 21:44:32 2016

@author: nacho
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path, os


def getHTML(url, user_agent):
    user = {'User-Agent': user_agent}
    try:
        html = requests.get(url, headers=user)
    except ConnectionError as e:
        print('Download error:', e.reason)
        html = None
    return html

def getBsObj(html):
    return BeautifulSoup(html.text, "html.parser")

def is_transport(transports, li):
    is_trans = False
    for transport in transports:
        if transport in li.find('span').get_text():
            is_trans = True
    return is_trans

def get_transport_url(li):
    return li.find('a').attrs['href']

def get_pages_download(transports, bsObj):
    pages_download = []
    transport_section = bsObj.find('div', {'id': 'contenido'})
    transport_section = transport_section.find('div', {'id': 'colIzda'})
    transport_section = transport_section.findAll('li')
    for li in transport_section:
        if is_transport(transports, li):
            pages_download.append(get_transport_url(li))
    return pages_download

def get_url_transport_lines(main_url, transport_pages):
    # Metro
    t = 0
    metro_lines = []
    url = main_url + transport_pages[t][1:]
    url = ".".join(url.split('.')[0:-1]) + '/lineas.aspx'

    html = getHTML(url, agent)
    bsObj = getBsObj(html)

    lineas = bsObj.find('div', {'class': 'listaBotones logosCuadrado dosCols'})
    lineas = lineas.findAll('li')
    for linea in lineas:
        line_url = linea.find('a').attrs['href']
        metro_lines.append(line_url)
    t += 1

    # Metro ligero
    ligero_lines = []
    url = main_url + transport_pages[t][1:]
    url = ".".join(url.split('.')[0:-1]) + '/lineas.aspx'

    html = getHTML(url, agent)
    bsObj = getBsObj(html)

    lineas = bsObj.find('div', {'class': 'listaBotones logosCuadrado dosCols'})
    lineas = lineas.findAll('li')
    for linea in lineas:
        line_url = linea.find('a').attrs['href']
        ligero_lines.append(line_url)
    t += 1

    # Cercanias
    cercania_lines = []
    url = main_url + transport_pages[t][1:]
    url = ".".join(url.split('.')[0:-1]) + '/lineas.aspx'

    html = getHTML(url, agent)
    bsObj = getBsObj(html)
    lineas = bsObj.find('div', {'class': 'listaBotones logosRectangulo unaCol'})
    lineas = lineas.findAll('li')
    for linea in lineas:
        line_url = linea.find('a').attrs['href']
        cercania_lines.append(line_url)
    t += 1

    return metro_lines, ligero_lines, cercania_lines

def get_stop_code_fromurl(url):
    stop_code = url.split('/')[-1]
    stop_code = stop_code.split('.')[0]
    stop_code = stop_code.split('_')[-1]
    return stop_code

def add_new_lineDF(df, new_line_data, columns):
    new_line = pd.DataFrame([new_line_data], columns=columns)
    frames = [df, new_line]
    df = pd.concat(frames, ignore_index=True)
    return df

def merge_dfs(df1, df2, colum):
    finaldf = pd.merge(df1, df2, on=colum)
    return finaldf

def concat_dfs(list_dfs):
    final_df = pd.concat(list_dfs, ignore_index=True)
    return final_df

def is_accesible(td):
    if td.find('img', {'alt': 'Logo de estación accesible'}):
        accessible = 'Yes'
    else:
        accessible = 'No'
    return accessible

def get_what_transport_links(td):
    initm = ""
    initml = ""
    initcr = ""
    delimiter = '/'
    transports_to_be_found = {'metro_linked': initm, 'ml_linked': initml, 'cr_linked': initcr}

    for span in td.findAll('span'):
        if span.attrs['class'][0].startswith('ml'):
            transports_to_be_found['ml_linked'] += delimiter + span.get_text()
        elif span.attrs['class'][0].startswith('c'):
            transports_to_be_found['cr_linked'] += delimiter + span.get_text()
        elif span.attrs['class'][0].startswith('m'):
            transports_to_be_found['metro_linked'] += delimiter + span.get_text()
    return transports_to_be_found

def there_is_parking(td):
    if td.find('img', {'alt': 'Logo de aparcamiento de disuasión de pago'}):
        parking = 'Yes'
    else:
        parking = 'No'
    return parking

def get_add_info_from_lines(info_toAdd, list_lines, columns, transport, main_url, cercanias=False):
    n_line = 1
    for t_line in list_lines:
        stop_order = 0
        html = getHTML(main_url[:-1] + t_line, agent)
        bsObj = getBsObj(html)
        lines_table = bsObj.find('table', {'class': 'tablaParadas'})
        ordered_line = lines_table.findAll('tr')
        for stop in ordered_line:
            try:
                # We set the transport
                transport_name = transport

                # We extract the stop url, in order to get info from each stop
                td = stop.findAll('td')

                # We extract the stop name
                stop_name = td[0].find('a').get_text()

                # We extract the stop code
                url = td[0].find('a').attrs['href']
                stop_code = get_stop_code_fromurl(url)

                # We extract the accesibilty
                accessible = is_accesible(td[1])

                # We extract the parking
                parking = there_is_parking(td[1])

                # We extract how they are linked among them
                transports_to_be_found = get_what_transport_links(td[2])

                stop_order += 1

                # Cercanías hasn got line 6, so we skip it
                if cercanias and n_line == 6:
                    n_line += 1

                start_string = 1
                new_line_toDF = [transport_name, stop_name, int(stop_code), str(int(n_line)),
                                 str(n_line) + '_' + str(stop_order), \
                                 transports_to_be_found['metro_linked'][start_string::], \
                                 transports_to_be_found['ml_linked'][start_string::], \
                                 transports_to_be_found['cr_linked'][start_string::], accessible, parking, main_url[:-1] + url]

                info_toAdd = add_new_lineDF(info_toAdd, new_line_toDF, columns)

            except AttributeError:
                pass
            except IndexError:
                pass
        n_line += 1
    return info_toAdd

def change_line_13_metro(df):
    df.loc[df['line_number'] == '13', 'line_number'] = 'R'
    df.loc[df['order_number'] == '13_1', 'order_number'] = 'R_1'
    df.loc[df['order_number'] == '13_2', 'order_number'] = 'R_2'
    return df

def fill_links_gaps(df):
    gap = 'No'
    df.loc[df['metro_linked'] == '', 'metro_linked'] = gap
    df.loc[df['ml_linked'] == '', 'ml_linked'] = gap
    df.loc[df['cr_linked'] == '', 'cr_linked'] = gap
    return df

def add_Valdebebas_station(df, columns):
    new_line_data = ['par_5_144', 144, 'Av. de las Fuerzas Armadas 322',\
                     40.4822881,-3.6184822,'A',0,'','Europe/Madrid',0]
    return add_new_lineDF(df, new_line_data, columns)

if __name__ == "__main__":
    # Main data
    main_url = 'http://www.crtm.es/'
    main_page = 'tu-transporte-publico.aspx'
    url_consor = main_url + main_page
    agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    transports = ['Metro', 'Metro Ligero', 'Cercanías']
    transport_ab = {'METRO': 'METRO', 'METRO_LIGERO': 'ML', 'CERCANIAS': 'CR'}

    columns = ['transportmean_name', 'stop_name', 'stop_code', 'line_number', 'order_number', 'metro_linked',
               'ml_linked', 'cr_linked', 'accesible', 'parking', 'stop_url']
    info_toAdd = pd.DataFrame(columns=columns)

    transport_pages = []
    metro_lines = []
    ligero_lines = []
    cercania_lines = []

    # We download the HTML and bsOBj of the main page
    html = getHTML(url_consor, agent)
    bsObj = getBsObj(html)

    # We get the page of each transport
    transport_pages = get_pages_download(transports, bsObj)

    # We get all the urls for each line of each transport
    metro_lines, ligero_lines, cercania_lines = get_url_transport_lines(main_url, transport_pages)

    # We build a DataFrame with the given columns, in order to merge this info
    # with the stops.txt info        
    info_toAdd = get_add_info_from_lines(info_toAdd, metro_lines, columns, transport_ab['METRO'], main_url)
    info_toAdd = get_add_info_from_lines(info_toAdd, ligero_lines, columns, transport_ab['METRO_LIGERO'], main_url)
    info_toAdd = get_add_info_from_lines(info_toAdd, cercania_lines, columns, transport_ab['CERCANIAS'], main_url, True)

    # We replace the line 13 of metro with R of Ramal
    info_toAdd = change_line_13_metro(info_toAdd)

    # We fill some gaps of transport links
    info_toAdd = fill_links_gaps(info_toAdd)

    # We open the stops.csv in order to be merged with the built one
    csv_namefile = 'stops.csv'
    stopsDF = pd.read_csv(csv_namefile)
    stopsDF.rename(columns={'\ufeffstop_id': 'stop_id'}, inplace=True)
    stopsDF.rename(columns={'wheelchair_boarding\n': 'wheelchair_boarding'}, inplace=True)

    # We split in different transports in order to work with stop_codes
    stopsDF_metro = stopsDF[(stopsDF.transportmean_name == transport_ab['METRO'])]
    stopsDF_ml = stopsDF[(stopsDF.transportmean_name == transport_ab['METRO_LIGERO'])]
    stopsDF_cr = stopsDF[(stopsDF.transportmean_name == transport_ab['CERCANIAS'])]

    infotoadd_metro = info_toAdd[(info_toAdd.transportmean_name == transport_ab['METRO'])]
    infotoadd_ml = info_toAdd[(info_toAdd.transportmean_name == transport_ab['METRO_LIGERO'])]

    # For this kind of transport, we will need to remove duplicates
    infotoadd_cr = info_toAdd[(info_toAdd.transportmean_name == transport_ab['CERCANIAS'])].drop_duplicates(
        subset='stop_code', keep='first')

    # We filter by location_type = 0. This value matches with a kind of stop
    stopsDF_metro = stopsDF_metro[(stopsDF_metro.location_type == 0)]
    stopsDF_ml = stopsDF_ml[(stopsDF_ml.location_type == 0)]
    stopsDF_cr = stopsDF_cr[(stopsDF_cr.location_type == 0)]

    # We fix column type mismatches
    stopsDF_ml.location_type = stopsDF_ml.location_type.astype(str)

    # We remove these columns in order to not have repeated columns in the final dataframe
    stopsDF_metro.drop('transportmean_name', axis=1, inplace=True)
    stopsDF_metro.drop('stop_name', axis=1, inplace=True)
    stopsDF_metro.drop('stop_url', axis=1, inplace=True)
    stopsDF_ml.drop('transportmean_name', axis=1, inplace=True)
    stopsDF_ml.drop('stop_name', axis=1, inplace=True)
    stopsDF_ml.drop('stop_url', axis=1, inplace=True)
    stopsDF_cr.drop('transportmean_name', axis=1, inplace=True)
    stopsDF_cr.drop('stop_name', axis=1, inplace=True)
    stopsDF_cr.drop('stop_url', axis=1, inplace=True)

    # We add the Valdebebas Station. It is not in stops.txt but it is a stop in the crtm page
    stopsDF_cr = add_Valdebebas_station(stopsDF_cr, stopsDF_cr.columns)

    # We merge the dfs of each transport
    finalDF_metro = merge_dfs(stopsDF_metro, infotoadd_metro, 'stop_code')
    finalDF_metro_ligero = merge_dfs(stopsDF_ml, infotoadd_ml, 'stop_code')
    finalDF_cercanias = merge_dfs(stopsDF_cr, infotoadd_cr, 'stop_code')

    # We sort by stop_id each dataframe
    order = ['line_number']
    finalDF_metro.sort_values(order, inplace = True)
    finalDF_metro_ligero.sort_values(order, inplace=True)
    finalDF_cercanias.sort_values(order, inplace=True)

    # We concat the DFs.
    list_dfs = [finalDF_metro, finalDF_metro_ligero, finalDF_cercanias]
    finalDF = concat_dfs(list_dfs)

    # We set the correct order to the columns
    finalcolumnsorder = ['transportmean_name', 'line_number', 'order_number', 'stop_id', 'stop_code', 'stop_name', \
                         'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', \
                         'location_type', 'parent_station', 'stop_timezone', 'wheelchair_boarding', 'metro_linked', \
                         'ml_linked', 'cr_linked', 'accesible', 'parking']
    finalDF = finalDF[finalcolumnsorder]

    # We export the result to a csv file
    finalDF.to_csv('Transports.csv', sep='\t')


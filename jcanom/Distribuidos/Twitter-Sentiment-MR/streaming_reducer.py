#!/usr/bin/env python
import sys

curr_zipcode = None
curr_count = 0
# Se lee el par <key,value> emitido por el mapper
for line in sys.stdin:

    # Obtenemos la key (cp) y el value (valoración)
    try:
        zipcode, count = line.split('\t')
        # Nos quedamos con los dos primeros dígitos del cp
        zipcode = zipcode[:2]
    except ValueError:
        print 'ValueError'
        
    count = float(count)
    # El primer cp se pone a sí mismo como actual
    if not(curr_zipcode):
        curr_zipcode = zipcode
    # Si el cp actual es el mismo que el anterior, actualiza el valor
    if zipcode == curr_zipcode:
        curr_count += count
    # Si no, emite la felicidad acumulada para ese cp y actualiza los acumulados
    else:     
        if curr_zipcode:
            print '{0}\t{1}'.format(curr_zipcode, curr_count)
            curr_zipcode = zipcode
            curr_count = count
    
# Emite el último cp
if curr_zipcode == zipcode:
    print '{0}\t{1}'.format(curr_zipcode, curr_count)


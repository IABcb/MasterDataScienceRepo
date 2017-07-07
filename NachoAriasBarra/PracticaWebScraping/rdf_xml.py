# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 21:50:20 2016

@author: nacho
"""

from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib import Namespace
import pandas as pd
import csv

if __name__ == "__main__":

    # Used ontologies:
    # xmlns:ns6="http://dublincore.org"
    # xmlns:ns3="http://xmlns.com/foaf/0.1"
    # xmlns:ns1="http://ontologi.es/rail/vocab"
    # xmlns:ns4="http://www.daml.org/2003/05/subway/subway-ont"
    # xmlns:ns7="http://schema.org"
    # xmlns:ns2="http://www.w3.org/2003/01/geo/wgs84_pos"
    # xmlns:ns5="http://e-tourism.deri.at/ont/e-tourism.owl"

    # Created ontologies:
    # xmlns:ns8="http://mytransportONT.org/linked_to_"

    data_path = "Transports.csv"
    data = pd.read_csv(data_path, delimiter='\t')

    g = Graph()

    # My ontology
    mytransportONT = Namespace("http://mytransportONT.org/")

    # General stop info
    is_stop_of = URIRef("http://dublincore.org/type")
    hasName = URIRef("http://xmlns.com/foaf/0.1/name")
    StationPosition = URIRef("http://ontologi.es/rail/vocab/StationPosition")
    belongstoLine = URIRef("http://www.daml.org/2003/05/subway/subway-ont/line")
    zoneId = URIRef("http://schema.org/areaServed")

    # Location
    hasAddress = URIRef("http://schema.org/address")
    haslat = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos/lat")
    haslong = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos/long")

    # Other info
    isAccesible = URIRef("http://schema.org/accessibilityFeature")
    hasparking = URIRef("http://e-tourism.deri.at/ont/e-tourism.owl/hasParking")

    for index, row in data.iterrows():

        stop = URIRef(row["stop_url"])

        # General stop info
        general_info_uri = "http://mytransportONT.org/general_info/" + str(row["stop_code"]) + 'ginfo'
        general_info = URIRef(general_info_uri)
        g.add((stop, mytransportONT.has_generalInfo, general_info))
        g.add((general_info, is_stop_of, Literal(row[1])))
        g.add((general_info, hasName, Literal(row[6])))
        g.add((general_info, belongstoLine, Literal(row[2])))
        g.add((general_info, StationPosition, Literal(row[3])))
        g.add((general_info, zoneId, Literal(row[10])))

        # Linked to
        link_uri = "http://mytransportONT.org/linked_to/" + str(row["stop_code"]) + 'link'
        links = URIRef(link_uri)
        g.add((stop, mytransportONT.linked_to, links))
        g.add((links, mytransportONT.has_metrolinks, Literal(row[16])))
        g.add((links, mytransportONT.has_mligerolinks, Literal(row[17])))
        g.add((links, mytransportONT.has_cercaniaslinks, Literal(row[18])))

        # Location
        location_uri = "http://mytransportONT.org/location/" + str(row["stop_code"]) + 'loc'
        location = URIRef(location_uri)
        g.add((stop, mytransportONT.haslocation, location))
        g.add((location, hasAddress, Literal(row[7])))

        coordinates_uri = "http://mytransportONT.org/coordinates/" + str(row["stop_code"]) + 'coords'
        coordinates = URIRef(coordinates_uri)
        g.add((location, mytransportONT.hasCoordinates, coordinates))
        g.add((coordinates, haslat, Literal(row[8])))
        g.add((coordinates, haslong, Literal(row[9])))

        # Other info
        infrastructure_uri = "http://mytransportONT.org/infrastructure/" + str(row["stop_code"]) + 'infra'
        infrastructure = URIRef(infrastructure_uri)
        g.add((stop, mytransportONT.hasinfrastructureInfo, infrastructure))
        g.add((infrastructure, hasparking, Literal(row[20])))
        g.add((infrastructure, isAccesible, Literal(row[19])))

    g.serialize(destination="estaciones.xml", format="xml")






















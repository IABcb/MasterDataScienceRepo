#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
os.system("docker run -itd --name=kafka -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST='localhost' --env ADVERTISED_PORT=9092 --env CONSUMER_THREADS=10 spotify/kafka")

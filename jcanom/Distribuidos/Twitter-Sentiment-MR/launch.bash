#! /bin/bash

 cat json/tweets_es_sample.json|./streaming_mapper.py|sort|./streaming_reducer.py > out.txt


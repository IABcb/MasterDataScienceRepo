#!/bin/bash

# Bash script to load all the JSON files of a folder into a MongoDB 
# collection. In order to use this script, set the wd of a terminal 
# in the folder where the JSON files are located, and type in the 
# terminal:
# ./load_documents.sh <dababase_name> <collection_name>
# Don't forget to set the load_documents.sh file as an executable

if [ "$#" -ne 2 ]; then
  echo "Invalid number of inputs arguments. Please, enter <dababase_name> and <collection_name>"
  exit 1
fi

# The database is deleted if already existing
mongo $1 --eval "db.dropDatabase()"

ls -1 *.json | sed 's/.json$//' | while read col; do 
    mongoimport --db $1 --collection $2 --file $col.json; 
done

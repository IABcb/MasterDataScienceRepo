# Welcome to the mongodb docker readme

# Download with:

sudo docker pull mongo

#  Source:
https://hub.docker.com/_/mongo/

# Steps to follow
1. Start mongo the way you prefer
2. Run it from command line, connected with another app. For python, just step 1.




# Start mongo
# Op1. Non-daemon

sudo docker run --rm --name my-mongo -v <path to folder where saving data>:/data/db -it -p 27017:27017 mongo:latest

sudo docker run --rm --name my-mongo -v /media/nacho/f8371289-0f00-4406-89db-d575f3cdb35e/Ericsson/Network_Slice_Selection_5Gproject/docker/mongodb/mongodata:/data/db -it -p 27017:27017 mongo:latest

# Op2. As a daemon

sudo docker run --name my-mongo -v <path to folder where saving data>:/data/db -d mongo:latest

sudo docker run --name my-mongo -v /media/nacho/f8371289-0f00-4406-89db-d575f3cdb35e/Ericsson/Network_Slice_Selection_5Gproject/docker/mongodb/mongodata:/data/db -d mongo:latest




# How to use it
# 1. From python

Please use pymongo library and Op1.

# 2. From command line 
sudo docker run -it --link my-mongo:mongo --rm mongo:latest sh -c 'exec mongo "$MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT/test"'

# 3. From an application
sudo docker run --name some-app --link my-mongo:mongo -d application-that-uses-mongo

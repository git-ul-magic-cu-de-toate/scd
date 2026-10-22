341C3 - Mihai Daniel Soare
Software Systems for Computer Networks

Homework 3 - IoT Platform using Microservices

January 2023

-------------


__Services__
------------

There are 5 available services in the `stack.yml` file:

- `mqtt-broker`
- `mmqtt-app`
- `mqtt-test`
- `influxdb`
- `grafana`

The services are deployed in a docker swarm node.

__`mqtt-broker`__

- is a broker of MQTT framework that has the official image of `eclipse-mosquitto`
- exposes port `1883` to other services

__`mqtt-app`__

- is a simple python application that uses the paho-mqtt module to connect to the `mqtt-broker` service and subscribe to any topics
- it will add the data received in the `influxdb` database in the `iot_database` bucket

__Project structure:__

```
mqtt-app/
├── app.env
├── Dockerfile
├── main.py
├── requirements.txt
├── server.py
└── startup.sh
```

- `Dockerfile` contains the rules needed to create a container with the application
- `startup.sh` is a file that runs when the container is created
- `main.py` is the main file that starts the application
- `.dockerignore` contains `.pyc` objects and other useless stuff that shouldn't be copied
when running the container
- `requirements.txt` contains all the modules needed to be installed on the container

__`mqtt-test`__

- is a simple python application that uses the paho-mqtt module to connect to
the `mqttt-broker` service and send topics and data for the `mqtt-app` service to collect

__``influxdb``__

- is a time series oriented database container on which the `mqtt-app` connect
and stores data received from the `mqtt-broker`
- has a volume to keep data after recreating it

__``grafana``__

- is an open source interactive vizualization app which has as data source: `influxdb` service and has by default 2 dashboards: `UPB IoT Dashboard`
and `Battery Dashboard`

- `UPB IoT Dashboard` has a graphic and a table, it collects data which are coming from `UPB` which is contained in the `measurement` field
- `Battery Dashboard` has a graphic that shows the data collected of the `BAT` tag and also a table that shows the `last value`, `mean`, `max`, `min`
values for each station

How to use the program
----------------------

__Commands__

- uses the script `run.sh` to initialize the docker swarm node and deploy the
services in the node.

__``grafana``__

- type `http://localhost/` in browser and connect with the credentials:
    - username: asistent
    - password: grafanaSPRC2023
    to see the dashboards created

** I have implemented all tasks from the homework sheet.
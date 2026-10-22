#!/bin/bash

mkdir -p volumes/influxdb-data
mkdir -p volumes/grafana-data

chmod o+w volumes/grafana-data

docker swarm init --advertise-addr 127.0.0.1

docker-compose -f stack.yml build
docker stack deploy -c stack.yml sprc3
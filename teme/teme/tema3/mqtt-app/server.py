import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pytz
import logging
import re
from os import getenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TIMEZONE = "Europe/Bucharest"

INFLUXDB_DB = getenv("INFLUXDB_DB")
INFLUXDB_HOST = getenv("INFLUXDB_HOST")
INFLUXDB_PORT = getenv("INFLUXDB_PORT")
INFLUXDB_URL = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}"
INFLUXDB_TOKEN = getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = getenv("INFLUXDB_ORG")

class MQTTServer():
    db_client: InfluxDBClient = None

    def __init__(self):
        logger_level = True
        if getenv("DEBUG_DATA_FLOW"):
            logger_level = logging.DEBUG
        else:
            logger_level = logging.INFO

        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logger_level
        )

    def get_timestamp(self, data):
        timestamp = None
        try:
            timestamp = datetime.strptime(data['timestamp'], TIME_FORMAT)
            logging.debug(f'Data timestamp is: {timestamp}')
        except:
            timestamp = datetime.strftime(datetime.now(pytz.timezone(TIMEZONE)), TIME_FORMAT)
            logging.debug('Data timestamp is NOW')

        return timestamp
            
    def on_message(self, client, args, msg):
        if not re.match(r'^[^\/]+\/[^\/]+$', msg.topic):
            return

        logging.debug(f"Received a message by topic [{msg.topic}]")

        data = json.loads(msg.payload)
        location, station = msg.topic.split("/") 
        timestamp = self.get_timestamp(data=data)

        for key, value in data.items():
            if not isinstance(value, int) and not isinstance(value, float) and key != "timestamp":
                continue
        
            entry = Point(f"{station}.{key}").tag("location", location).tag("station", station).field("value", float(value)).time(timestamp)
            
            write_api = self.db_client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=INFLUXDB_DB, org=INFLUXDB_ORG, record=entry)

            logging.debug(f'{location}.{station}.{key} {value}')

    def run(self):
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = self.on_message

        self.db_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

        mqtt_client.connect(getenv("BROKER"), 1883)
        mqtt_client.subscribe("#")
        mqtt_client.loop_forever()

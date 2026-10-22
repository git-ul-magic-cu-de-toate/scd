from json import dumps
from numpy import arange
from random import choice
from time import sleep
import paho.mqtt.client as mqtt

def main():
	client = mqtt.Client()
	client.connect("mqtt-broker", 1883)
	client.loop_start()

	batteries = list(range(80, 110))
	temperatures = list(range(15, 31))
	humid = list(range(25, 41))
	seconds = list(arange(0.7, 1.3, 0.1))
	stations = ['Gas', 'Mongo']

	count = 1
	while True:
		count += 1
		iot_data = {
			'BAT': choice(batteries),
			'TEMP': choice(temperatures),
			'HUMID': choice(humid),
		}

		station = choice(stations)

		client.publish('UPB/' + station, dumps(iot_data))

		if count == 5:
			sleep(choice(seconds))
			station = "Yuki"
			client.publish('Ramsi/' + station, dumps(iot_data))

		print(f'Station {station} published:\n{dumps(iot_data, indent=4)}\n')

		sleep(choice(seconds))

		if count == 10:
			break

	client.disconnect()
	client.loop_stop()


if __name__ == "__main__":
	main()
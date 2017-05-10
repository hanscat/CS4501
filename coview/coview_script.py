from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, time

try:
    # wait for 30 seconds for the initialization of Kafka
    time.sleep(30)

    CVconsumer = KafkaConsumer('car-views', group_id='carview-indexer', bootstrap_servers=['kafka:9092'])

finally:

	CVconsumer = KafkaConsumer('car-views', group_id='carview-indexer', bootstrap_servers=['kafka:9092'])
	logfile = open("log.txt", "a")

	while True:
		for message in CVconsumer:
			new_view = (json.loads(message.value.decode('utf-8'))) 
			user_id = new_view['user_id']
			car_id = new_view['car_id']['id']
			logfile = open("log.txt", "a")
			logfile.write(str(user_id) + " " + str(car_id) + '\n')
			logfile.close()


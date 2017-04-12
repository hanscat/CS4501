from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, time

try:
    # wait for 30 seconds for the initialization of Kafka
    time.sleep(30)

    # try to create instances of Kafka and Elasticsearch
    es = Elasticsearch(['es'])
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

finally:
	# initialize the Elasticsearch instance
    es = Elasticsearch(['es'])
	# Load fixture into elastic search
    data = {}
    with open('demo.json') as data_file:
        data = json.load(data_file)

    for element in data:
        if 'password' in element['fields']:
            element['fields'].pop('password', None)

        element['fields']['id'] = element['pk']
        # Model Specific Indices
        if element['model'] == 'api.car':
            es.index(index='car_index', doc_type='listing', id=element['pk'], body=element)
            es.index(index='general_index', doc_type='listing', id=element['pk'], body=element)

        elif element['model'] == 'api.user':
            es.index(index='user_index', doc_type='listing', id=element['pk'], body=element)
            es.index(index='general_index', doc_type='listing', id=element['pk'], body=element)

    es.indices.refresh(index="user_index")
    es.indices.refresh(index="car_index")
    es.indices.refresh(index="general_index")

    # Start listening to Kafka Queue
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

    while True:
        for message in consumer:
            new_listing = (json.loads(message.value.decode('utf-8')))
            # Model Specific Indices
            if new_listing['model'] == 'api.car':
                es.index(index='car_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
                es.index(index='general_index', doc_type='listing', id=new_listing['pk'] * 2, body=new_listing)

            elif new_listing['model'] == 'api.user':
                es.index(index='user_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
                es.index(index='general_index', doc_type='listing', id=new_listing['pk'] * 2 + 1, body=new_listing)

        # refresh all incides to make changes effective
            es.indices.refresh(index="user_index")
            es.indices.refresh(index="car_index")
            es.indices.refresh(index="general_index")

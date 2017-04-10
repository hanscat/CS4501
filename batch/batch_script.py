
import sched, time
from kafka import KafkaConsumer
import sched, time
from elasticsearch import Elasticsearch
import json

es = Elasticsearch([{'host': 'es', 'port': 9200}])

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
	consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
	for message in consumer:
		new_listing = json.loads((message.value).decode('utf-8'))
		# if(new_listing['m'])
		# test if success
		# print(new_listing)
		if(new_listing['model']=='user'):
			ret = es.index(index='listing_index', doc_type='listing', id=new_listing['username'], body=new_listing)
		else:
			ret = es.index(index='listing_index', doc_type='listing', id=new_listing['model'], body=new_listing)
	es.indices.refresh(index="listing_index")

	s.enter(10, 1, do_something, (sc,))

s.enter(10, 1, do_something, (s,))
s.run()
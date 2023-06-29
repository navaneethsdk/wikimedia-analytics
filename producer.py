import requests
from kafka import KafkaProducer
import json
from sseclient import SSEClient as EventSource

# url of wikimedia stream
URL = "https://stream.wikimedia.org/v2/stream/recentchange"

# Kafka topic to produce to
TOPIC = "wikimedia-events"

# Kafka cluster address
BOOTSTRAP_SERVERS = "localhost:9092"

# Create Kafka producer
producer = KafkaProducer(
	bootstrap_servers=BOOTSTRAP_SERVERS,
	value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

for event in EventSource(URL):
	if event.event == "message":
		try:
			event_data = json.loads(event.data)
		except ValueError:
			pass
		else:
			data_to_write = {
				"title": event_data["title"],
				"timestamp": event_data["timestamp"],
				"server_name": event_data["server_name"],
				"bot": event_data["bot"],
				"type": event_data["type"],
			}

			# Produce data to Kafka topic
			producer.send(TOPIC, value=data_to_write)
			producer.flush()
				

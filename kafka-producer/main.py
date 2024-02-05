from kafka import KafkaProducer
import json
import time
from event import Event

# Define Kafka Configuration
# Move values later to configuration file
kafka_config = {"bootstrap_servers": "localhost:9092", "client_id": "python-producer"}

# Define Kafka Topic
kafka_topic = "my_topic"

# Create Kafka producer instance
producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode("utf-8"), **kafka_config
)


try:
    # change it later
    reporter_id = 0

    while True:
        reporter_id += 1
        event = Event(reporter_id)
        event_json = event.to_json()

        # Produce the event to kafka
        producer.send(kafka_topic, key=str(reporter_id), value=event_json)

        # wait 1 second before producing the next event
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    producer.close()
import json
import time
import configparser
from kafka import KafkaProducer
from event import Event


# Read configuration from configuration.ini file
config = configparser.ConfigParser()
config.read('configuration.ini')

# Define Kafka Configuration
# Move values later to configuration file
kafka_config = {
    "bootstrap_servers": config.get("Kafka", "bootstrap_servers"),
    "client_id": config.get("Kafka", "client_id")
}

# Define Kafka Topic
kafka_topic = config.get("Kafka", "topic")

# Create Kafka producer instance
producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode("utf-8"), **kafka_config
)


try:
    while True:
        event = Event()
        event_json = event.to_json()

        # Produce the event to kafka
        producer.send(kafka_topic, key=str(event.reporter_id), value=event_json)

        # Increment reporter_id for the next event
        event.reporter_id += config.getint("event", "reporter_id_increment")

        # wait 1 second before producing the next event
        time.sleep(config.getint("Event", "sleep_time_seconds"))
except KeyboardInterrupt:
    pass
finally:
    producer.close()

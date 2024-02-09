import json
import time
from kafka import KafkaProducer
from event import Event
from config_loader import config
from logger import logger


# Define Kafka Topic
kafka_topic = config["Kafka"]["topic"]

# Create Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=config["Kafka"]["bootstrap_servers"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    client_id=config["Kafka"]["client_id"],
    api_version=tuple(map(int, config["Kafka"]["api_version"].strip("()").split(","))),
)

# Initialize reporter_id
global_reporter_id = config["Event"]["initial_reporter_id"]

try:
    while True:
        event = Event()
        event.reporter_id = global_reporter_id
        event_json = event.to_json()
        print(f"Producing event: {event_json}")

        # Produce the event to kafka
        producer.send(kafka_topic, event_json)

        # Flush the producer to ensure all messages are sent to Kafka before continuing
        producer.flush()

        # Increment reporter_id for the next event
        global_reporter_id += config["Event"]["reporter_id_increment"]

        # wait 1 second before producing the next event
        time.sleep(config["Event"]["sleep_time_seconds"])
except Exception as e:
    print(f"Error in Kafka producer: {e}")
    logger.exception(f"Error in Kafka producer: {e}")
finally:
    producer.close()

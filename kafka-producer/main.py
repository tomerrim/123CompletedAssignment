import json
import time
import configparser
from kafka import KafkaProducer
from event import Event


# Read configuration from configuration.ini file
config = configparser.ConfigParser()
config.read('configuration.ini')

# Define Kafka Topic
kafka_topic = config.get("Kafka", "topic")

# Create Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=config.get("Kafka", "bootstrap_servers"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    api_version=tuple(
        map(int, config.get("Kafka", "api_version").strip("()").split(","))
    ),
    client_id=config.get("Kafka", "client_id"),
)

# Initialize reporter_id
global_reporter_id = config.getint("Event", "initial_reporter_id")

try:
    while True:
        event = Event()
        event.reporter_id = global_reporter_id
        event_json = event.to_json()
        print(f"Producing event: {event_json}")

        # Produce the event to kafka
        producer.send(kafka_topic, event_json)
        producer.flush()

        # Increment reporter_id for the next event
        global_reporter_id += config.getint("Event", "reporter_id_increment")
        print(f"reporter_id: {global_reporter_id}")

        # wait 1 second before producing the next event
        time.sleep(config.getint("Event", "sleep_time_seconds"))
except Exception as e:
    print(f"Error in Kafka producer: {e}")
finally:
    producer.close()

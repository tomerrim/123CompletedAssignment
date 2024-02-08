from kafka import KafkaConsumer
import json
from datetime import datetime
from pymongo import MongoClient
from config_loader import config


# Kafka consumer configuration
kafka_bootstrap_servers = config["Kafka"]["bootstrap_servers"]
kafka_topic = config["Kafka"]["topic"]
kafka_auto_offset_reset = config["Kafka"]["auto_offset_reset"]
kafka_api_version = tuple(map(int, config["Kafka"]["api_version"].strip("()").split(",")))

# MongoDB configuration
mongo_uri = config["MongoDB"]["mongodb_uri"]
mongo_db_name = config["MongoDB"]["db_name"]
mongo_collection_name = config["MongoDB"]["collection_name"]

# Create MongoDB client and connect to the database
client = MongoClient(mongo_uri)
db = client[mongo_db_name]
events_collection = db[mongo_collection_name]

# Create Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    auto_offset_reset=kafka_auto_offset_reset,  # Start consuming from the beginning of the topic
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    api_version=kafka_api_version
)

try:
    # Continuously consume messages
    for message in consumer:
        event = message.value
        print("Received message:", event)

        # Convert timestamp string to datetime object
        event['timestamp'] = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S')

        # Insert event into MongoDB
        events_collection.insert_one(event)
        print(f"inserted to {events_collection}")
except Exception as e:
    print(f"Error in Kafka consumer or MongoDB insertion: {e}")
finally:
    consumer.close()
    client.close()

from kafka import KafkaConsumer
import json
import configparser
from datetime import datetime
from pymongo import MongoClient

# Read configuration from configuration.ini file
config = configparser.ConfigParser()
config.read("configuration.ini")


# Kafka consumer configuration
kafka_bootstrap_servers = config.get("Kafka", "bootstrap_servers")
kafka_topic = config.get("Kafka", "topic")
kafka_auto_offset_reset = config.get("Kafka", "auto_offset_reset")
kafka_api_version = tuple(
    map(int, config.get("Kafka", "api_version").strip("()").split(","))
)

# MongoDB configuration
mongo_uri = config.get("MongoDB", "mongodb_uri")
mongo_db_name = config.get("MongoDB", "db_name")
mongo_collection_name = config.get("MongoDB", "collection_name")

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
except Exception as e:
    print(f"Error in Kafka consumer or MongoDB insertion: {e}")
finally:
    consumer.close()
    client.close()

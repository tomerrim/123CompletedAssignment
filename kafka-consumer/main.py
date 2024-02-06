from kafka import KafkaConsumer
import json
import configparser

# Read configuration from configuration.ini file
config = configparser.ConfigParser()
config.read("configuration.ini")


# Kafka consumer configuration
kafka_bootstrap_servers = config.get("Kafka", "bootstrap_servers")
kafka_topic = config.get("Kafka", "topic")
kafka_auto_offset_reset = config.get("Kafka", "auto_offset_reset")
kafka_api_version = config.get("Kafka", "api_version")

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
        print("Received message:", message.value)
except Exception as e:
    print(f"Error in Kafka consumer: {e}")
finally:
    consumer.close()

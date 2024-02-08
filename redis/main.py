import json
import threading
import time
from pymongo import MongoClient
from config_loader import config
from redis import Redis
from datetime import datetime

# MongoDB configuration
mongo_uri = config["MongoDB"]["mongodb_uri"]
mongo_db_name = config["MongoDB"]["db_name"]
mongo_collection_name = config["MongoDB"]["collection_name"]

# Create MongoDB client and connect to the database
mongo_client = MongoClient(mongo_uri)
db = mongo_client[mongo_db_name]
events_collection = db[mongo_collection_name]

# Redis configuration
redis_host = config["Redis"]["host"]
redis_port = config["Redis"]["port"]
redis_sleep_time_seconds = config["Redis"]["sleep_time_seconds"]

timestamp_format = config["Event"]["timestamp_format"]

# Create Redis client
redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

def main():
    etl_thread = threading.Thread(target=run_etl_process, args=(mongo_client,redis_client))
    etl_thread.start()


def run_etl_process(mongo_client, redis_client):
    while True:
        extract_transform_load(mongo_client, redis_client)
        time.sleep(redis_sleep_time_seconds)


def extract_transform_load(mongo_client, redis_client):
    latest_timestamp = get_latest_timestamp(redis_client)
    new_data_cursor = events_collection.find({"timestamp": {"$gt": latest_timestamp}}).sort("timestamp", 1)
    for data in new_data_cursor:
        redis_key = f"{data['reporterId']}:{data['timestamp'].strftime(timestamp_format)}"
        redis_value = json.dumps(data)
        redis_client.set(redis_key, redis_value)


def get_latest_timestamp(redis_client):
    try:
        keys = redis_client.keys(pattern='*:*')
        timestamps = [datetime.strftime(key.decode('utf-8').split(':')[1], timestamp_format) for key in keys]
        return max(timestamps) if timestamps else datetime.min
    except Exception as e:
        print(f"Error retrieving latest timestamp from Redis: {e}")
        return datetime.min


if  __name__ == "__main__":
    main()
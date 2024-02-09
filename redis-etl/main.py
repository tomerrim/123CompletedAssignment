import json
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
timestamp = config["Event"]["timestamp"]

# Create Redis client
redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

def main():
    while True:
        extract_transform_load(mongo_client, redis_client)
        time.sleep(redis_sleep_time_seconds)


def extract_transform_load(mongo_client, redis_client):
    latest_timestamp = get_latest_timestamp()
    timestamp_query = {timestamp: {"$gt": latest_timestamp}} if latest_timestamp else {}
    new_data_cursor = list(events_collection.find(timestamp_query).sort(timestamp, 1))
    for data in new_data_cursor:
        redis_key = f"{data['reporterId']}:{datetime.strftime(data[timestamp],timestamp_format)}"
        redis_value = json.dumps(data, default=str)
        redis_client.set(redis_key, redis_value)
        set_latest_timestamp(data[timestamp])
        print(f"object with key {redis_key} inserted to redis database")


def get_latest_timestamp():
    try:
        latest_timestamp = redis_client.get('latest_timestamp')
        latest = datetime.strptime(latest_timestamp, timestamp_format)
        return latest if latest_timestamp else None
    except Exception as e:
        print(f"Error retrieving latest timestamp from Redis: {e}")
        return datetime.min


def set_latest_timestamp(timestamp):
    redis_client.set('latest_timestamp', timestamp.strftime(timestamp_format))


if  __name__ == "__main__":
    main()

# 123 Completed Assignment

## Overview
This project implements a distributed event processing system using Kafka, MongoDB, Redis, and Docker. It consists of a Kafka producer that generates events, a Kafka consumer that processes these events and stores them in MongoDB, and an ETL service that transfers data from MongoDB to Redis.

## Components
- **Kafka Producer**: Generates and sends events to a Kafka topic. Each event includes a reporter ID, timestamp, metric ID, metric value, and a message.
- **Kafka Consumer**: Listens to the Kafka topic and processes incoming events. The processed events are then stored in MongoDB.
- **MongoDB**: Serves as the primary data store for events consumed from Kafka.
- **Redis**: Used as a secondary data store and cache to hold the processed data from MongoDB.
- **Redis-ETL Service**: Periodically extracts new data from MongoDB, transforms it, and loads it into Redis. This service ensures that only new events are transferred to Redis based on the timestamps.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites
- Docker and Docker Compose
- Python 3.8 or higher

### Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run `docker-compose up -d` to start all the services in detached mode.
4. The Kafka producer and consumer, along with the MongoDB and Redis services, should now be running.

## Built With
- [Python](https://www.python.org/) - The programming language used.
- [Docker](https://www.docker.com/) - Containerization platform.
- [Kafka](https://kafka.apache.org/) - Distributed event streaming platform.
- [MongoDB](https://www.mongodb.com/) - NoSQL database.
- [Redis](https://redis.io/) - In-memory data structure store.

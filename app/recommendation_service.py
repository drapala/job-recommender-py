from kafka import KafkaProducer
from pymongo import MongoClient
import os

# Kafka settings
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')

# MongoDB settings
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))

# Function to get Kafka producer
def get_kafka_producer():
    """
    Creates and returns a Kafka producer.
    """
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
        return producer
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        raise

# Function to get MongoDB client
def get_mongo_client():
    """
    Creates and returns a MongoDB client.
    """
    try:
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

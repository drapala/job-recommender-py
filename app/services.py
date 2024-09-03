import json
from flask import current_app
from pymongo import MongoClient
from kafka import KafkaProducer

def get_mongo_client():
    mongo_client = MongoClient(current_app.config['MONGO_HOST'], current_app.config['MONGO_PORT'])
    return mongo_client[current_app.config['MONGO_DB']]

def get_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers=current_app.config['KAFKA_BROKER'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

def generate_recommendations():
    mongo_db = get_mongo_client()
    job_data = list(mongo_db['jobs'].find())

    recommendations = [{'job': job['title'], 'score': 90} for job in job_data]

    producer = get_kafka_producer()
    for recommendation in recommendations:
        producer.send(current_app.config['KAFKA_TOPIC'], recommendation)

    producer.flush()
    return recommendations

import json
from flask import current_app
from pymongo import MongoClient
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time

class RecommendationService:
    def __init__(self):
        """
        Initialize the Recommendation Service.
        """
        self.mongo_client = None
        self.kafka_producer = None

    def get_mongo_client(self):
        """
        Initialize and return the MongoDB client.
        """
        if not self.mongo_client:
            try:
                self.mongo_client = MongoClient(current_app.config['MONGO_HOST'], current_app.config['MONGO_PORT'])
                return self.mongo_client[current_app.config['MONGO_DB']]
            except Exception as e:
                current_app.logger.error(f"Error connecting to MongoDB: {e}")
                raise
        return self.mongo_client[current_app.config['MONGO_DB']]

    def get_kafka_producer(self):
        """
        Initialize and return the Kafka producer.
        """
        if not self.kafka_producer:
            try:
                self.kafka_producer = KafkaProducer(
                    bootstrap_servers=current_app.config['KAFKA_BROKER'],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
            except Exception as e:
                current_app.logger.error(f"Error creating Kafka producer: {e}")
                raise
        return self.kafka_producer

    def publish_event(self, event_type, event_data):
        """
        Function to publish events to Kafka.
        """
        event = {'type': event_type, 'data': event_data}
        try:
            producer = self.get_kafka_producer()
            producer.send(current_app.config['KAFKA_TOPIC'], value=event)
            producer.flush()
            current_app.logger.info(f"Event {event_type} published successfully.")
        except KafkaError as e:
            current_app.logger.error(f"Error publishing the event: {e}")
            raise

    def generate_recommendations(self):
        """
        Generate recommendations and publish them to Kafka.
        """
        producer = None  # Initialize the producer variable
        try:
            # Initialize the MongoDB client and fetch data
            mongo_db = self.get_mongo_client()
            job_data = list(mongo_db['jobs'].find())

            # Generate recommendations based on the data
            recommendations = [{'job': job['title'], 'score': 90} for job in job_data]

            # Initialize the Kafka producer
            producer = self.get_kafka_producer()

            # Send each recommendation to Kafka
            for recommendation in recommendations:
                retries = 3  # Number of retries for sending to Kafka
                for attempt in range(retries):
                    try:
                        producer.send(current_app.config['KAFKA_TOPIC'], value=recommendation)
                        current_app.logger.info(f"Recommendation sent: {recommendation}")
                        break  # If sending is successful, break out of the retry loop
                    except KafkaError as e:
                        current_app.logger.error(f"Error sending recommendation on attempt {attempt + 1}: {e}")
                        if attempt < retries - 1:
                            time.sleep(2 ** attempt)  # Exponential backoff
                        else:
                            current_app.logger.error(f"Failed to send recommendation after {retries} attempts.")

            # Make sure all messages are sent
            producer.flush()
            return recommendations
        except Exception as e:
            current_app.logger.error(f"Error generating recommendations: {e}")
            raise
        finally:
            # Close the producer to release resources if it was initialized
            if producer:
                producer.close()

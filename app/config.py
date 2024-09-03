import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'dev_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'dev_password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'job_db')

    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    MONGO_DB = os.getenv('MONGO_DB', 'job_recommendations')

    KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'job-recommendations')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

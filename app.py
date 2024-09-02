import os
import json
import atexit
from flask import Flask, jsonify, request
from pymongo import MongoClient
import pymysql
from kafka import KafkaProducer

app = Flask(__name__)

# Carregar configurações do ambiente
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'dev_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'dev_password')
MYSQL_DB = os.getenv('MYSQL_DB', 'job_db')

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_DB = os.getenv('MONGO_DB', 'job_recommendations')

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'job-recommendations')

# Inicializar conexões fora das rotas
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
mongo_db = mongo_client[MONGO_DB]

mysql_connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def close_connections():
    """Função para fechar conexões ao encerrar a aplicação."""
    app.logger.info('Fechando conexões...')
    mysql_connection.close()
    mongo_client.close()
    producer.close()

atexit.register(close_connections)

@app.route('/generate_recommendations', methods=['POST'])
def generate_recommendations():
    try:
        # Exemplo de leitura de dados do MongoDB
        job_data = list(mongo_db['jobs'].find())

        # Lógica para gerar recomendações
        recommendations = [{'job': job['title'], 'score': 90} for job in job_data]

        # Publicar no Kafka
        for recommendation in recommendations:
            producer.send(KAFKA_TOPIC, recommendation)

        return jsonify({'status': 'success', 'data': recommendations})

    except Exception as e:
        # Log de erro e resposta
        app.logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        # Fechar o produtor Kafka após o envio
        producer.flush()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

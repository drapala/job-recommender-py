app = Flask(__name__)

# Configurações do banco de dados
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'job_db'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'job_recommendations'

# Configurações do Kafka
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'job-recommendations'

# Conectar ao MongoDB
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
mongo_db = mongo_client[MONGO_DB]

# Conectar ao MySQL
mysql_connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB
)

# Criar produtor Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/generate_recommendations', methods=['POST'])
def generate_recommendations():
    # Exemplo de leitura de dados do MongoDB
    job_data = list(mongo_db['jobs'].find())

    # Lógica para gerar recomendações (simples exemplo)
    recommendations = [{'job': job['title'], 'score': 90} for job in job_data]

    # Publicar no Kafka
    for recommendation in recommendations:
        producer.send(KAFKA_TOPIC, recommendation)

    return jsonify({'status': 'success', 'data': recommendations})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
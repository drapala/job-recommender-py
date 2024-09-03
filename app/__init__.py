from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_healthz import healthz
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from .config import Config
from .routes import register_blueprints
from .models import db
from . import recommendation_service

# Extension initialization
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    register_blueprints(app)

    # Add health checks
    app.register_blueprint(healthz, url_prefix="/healthz")

    @app.route("/healthz/liveness")
    def liveness():
        # A simple check that the application is alive
        return "Service is alive", 200

    @app.route("/healthz/readiness")
    def readiness():
        try:
            # Kafka verification
            kafka_producer = recommendation_service.get_kafka_producer()
            kafka_producer.send('health-check', b'')
            kafka_producer.flush()
            print("Kafka is available.")

            # MySQL verification
            mysql_connection = db.engine.connect()
            mysql_connection.execute('SELECT 1')
            print("MySQL is available.")

            # MongoDB verification
            mongo_client = recommendation_service.get_mongo_client()
            mongo_client.server_info()
            print("MongoDB is available.")

            return "Service is healthy", 200
        except Exception as e:
            print(f"Health check error: {e}")
            return "Service is unhealthy", 503

    # Configuration and Instrumentation with OpenTelemetry
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    otlp_exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    FlaskInstrumentor().instrument_app(app)

    return app

app = create_app()

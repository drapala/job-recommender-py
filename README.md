# Job Recommender Service - Python (Flask)

This microservice is part of the "Multistack Real-Time Job Recommendation Engine" and is responsible for capturing user events, managing sessions, interacting with MySQL and MongoDB databases, and publishing recommendation events to Kafka.

## Requirements

- Python 3.8+
- Pip (Python package manager)
- Docker and Docker Compose
- Apache Kafka
- MySQL Database
- MongoDB

## Configuration

### Local Setup Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/drapala/job-recommender-py.git
   cd job-recommender-py
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Database configuration:**

   Check the MySQL and MongoDB connection settings in the `app.py` file:

   ```python
   MYSQL_HOST = 'localhost'
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'password'
   MYSQL_DB = 'job_db'

   MONGO_HOST = 'localhost'
   MONGO_PORT = 27017
   MONGO_DB = 'job_recommendations'

   KAFKA_BROKER = 'localhost:9092'
   ```

4. **Run the service:**

   Start the Flask server:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

## Usage

- **API REST Endpoints:**
  - `POST /generate_recommendations`: Generate job recommendations and publish to Kafka.

## Docker

### Building and Running with Docker

1. **Build the Docker image:**

   ```bash
   docker build -t job-recommender-py .
   ```

2. **Run the container:**

   ```bash
   docker run -p 5000:5000 job-recommender-py
   ```

## Contributing

Contributions are welcome! Please fork the repository and open a pull request with your improvements or fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

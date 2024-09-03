# Job Recommender Service - Python (Flask)
# Multistack Real-Time Job Recommendation Engine

This repository contains a microservice that is part of the "Multistack Real-Time Job Recommendation Engine". This microservice is responsible for capturing user events, managing sessions, interacting with MySQL and MongoDB databases, and publishing recommendation events to Kafka.

## Requirements

To run this project, you need the following:

- Python 3.8+
- Pip (Python package manager)
- Docker and Docker Compose
- Apache Kafka
- MySQL Database
- MongoDB

## Configuration

### Local Setup Steps

Follow these steps to set up the project locally:

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

   Update the MySQL and MongoDB connection settings in the `app.py` file:

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
  - `POST /users`: Create a new user.
  - `GET /users/{user_id}`: Get a user by ID.
  - `GET /users`: Get all users.
  - `PUT /users/{user_id}`: Update a user by ID.
  - `DELETE /users/{user_id}`: Delete a user by ID.
  - `POST /generate_recommendations`: Generate job recommendations and publish them to Kafka.
  - `POST /activity`: Create a new activity.
  - `GET /activity/{activity_id}`: Get an activity by ID.
  - `GET /activity`: Get all activities.
  - `PUT /activity/{activity_id}`: Update an activity by ID.
  - `DELETE /activity/{activity_id}`: Delete an activity by ID.
  - `POST /job`: Create a new job.
  - `GET /job/{job_id}`: Get a job by ID.
  - `GET /job`: Get all jobs.
  - `PUT /job/{job_id}`: Update a job by ID.
  - `DELETE /job/{job_id}`: Delete a job by ID.

## Docker

### Building and Running with Docker

To run the project using Docker, follow these steps:

1. **Build the Docker image:**

   ```bash
   docker build -t job-recommender-py .
   ```

2. **Run the container:**

   ```bash
   docker run -p 5000:5000 job-recommender-py
   ```

## Contributing

Contributions are welcome! If you have any improvements or fixes, please fork the repository and open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.


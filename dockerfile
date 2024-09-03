FROM python:3.9-slim

# Install the MySQL client
RUN apt-get update && apt-get install -y default-mysql-client netcat-openbsd

# Set the working directory
WORKDIR /app

# Copy the requirements.txt to install dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the wait script
COPY wait-for-mysql.sh /wait-for-mysql.sh

# Make the wait script executable
RUN chmod +x /wait-for-mysql.sh

# Expose the port on which Flask is running
EXPOSE 5000

# Command to run the application using the wait script
CMD ["/wait-for-mysql.sh", "mysql", "python", "app.py"]

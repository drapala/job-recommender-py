FROM python:3.9-slim

RUN apt-get update && apt-get install -y default-mysql-client netcat-openbsd

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-mysql.sh /wait-for-mysql.sh

RUN chmod +x /wait-for-mysql.sh

EXPOSE 5000

CMD ["/wait-for-mysql.sh", "mysql", "python", "run.py"]

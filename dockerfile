FROM python:3.9-slim

RUN apt-get update && apt-get install -y default-mysql-client netcat-openbsd

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

RUN pip install kafka-python six

COPY . .

COPY wait-for-mysql.sh /wait-for-mysql.sh

RUN chmod +x /wait-for-mysql.sh

EXPOSE 5000

ENV FLASK_APP=app:create_app
ENV FLASK_DEBUG=1

CMD ["/wait-for-mysql.sh", "mysql", "flask", "run", "--host=0.0.0.0"]

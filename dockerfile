FROM python:3.7-slim

WORKDIR /app

COPY database_writing.py /app/database_writing.py
COPY requirements.txt /app/requirements.txt
COPY data.json /app/data.json

RUN ["pip", "install", "-r","./requirements.txt"]
CMD ["python", "./database_writing.py"]
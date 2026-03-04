FROM python:3.11-slim
WORKDIR /app
COPY server.py .
COPY client.py .
CMD ["python", "server.py"]
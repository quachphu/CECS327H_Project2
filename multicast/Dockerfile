FROM python:3.11-slim
WORKDIR /app
COPY multicast_sender.py .
COPY multicast_receiver.py .
CMD ["python", "multicast_receiver.py"]
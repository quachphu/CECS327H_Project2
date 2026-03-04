# Dockerfile - Container image for Anycast TCP Server and Client (Task 1)
# CECS 327 - Project 2: A Bite of Distributed Communication
#
# Uses a lightweight Python 3.11 slim image to minimize container size.
# Only the standard library is needed (socket module), so no pip installs
# are required.

# Base image: Python 3.11 on Debian slim (small footprint)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all Python source files into the container
COPY server.py .
COPY client.py .

# Default command — overridden per service in docker-compose.yml
# Server containers run server.py; the client container runs client.py.
CMD ["python", "server.py"]
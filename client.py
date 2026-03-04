"""
client.py - TCP Client for Anycast Simulation (Task 1)
CECS 327 - Project 2: A Bite of Distributed Communication

This client connects to the Docker service hostname "server" on port 5000.
Docker's embedded DNS performs round-robin resolution, so each connection
may reach a different server container — simulating Anycast behavior.

The client makes multiple connection attempts (default 6) with a short
delay between each, demonstrating that different servers handle different
requests.

How Anycast simulation works:
    - All 3 server containers register under the same Docker Compose
      service name ("server").
    - Docker's internal DNS returns one of the container IPs at random
      for each lookup of "server".
    - The client therefore "randomly" reaches server1, server2, or server3.
"""

import socket
import time

# Docker Compose service name — Docker DNS resolves this to one of the
# server container IPs via round-robin.
SERVER_HOST = "server"
SERVER_PORT = 5000

# Number of times the client will connect to demonstrate load balancing
NUM_ATTEMPTS = 6

# Seconds to wait between connection attempts
DELAY = 1


def connect_once():
    """
    Opens a single TCP connection to the server service, receives the
    greeting message, prints it, and closes the connection.

    Returns:
        str: The message received from the server, or None on failure.
    """
    try:
        # Create a new TCP socket for each connection attempt
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout so the client doesn't hang forever if no server responds
        client_socket.settimeout(5)

        # Connect to the Docker DNS-resolved server address
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Receive up to 1024 bytes of data from the server
        data = client_socket.recv(1024)
        message = data.decode("utf-8")
        print(f"Received: {message}")

        # Clean up the socket
        client_socket.close()
        return message

    except Exception as e:
        print(f"Connection error: {e}")
        return None


def main():
    """
    Runs multiple connection attempts to demonstrate Anycast-like behavior.
    After all attempts, prints a summary of which servers were reached.
    """
    print(f"Anycast client starting — will connect {NUM_ATTEMPTS} times\n")

    # Wait briefly for servers to be ready on first run
    time.sleep(2)

    results = []
    for i in range(NUM_ATTEMPTS):
        print(f"--- Attempt {i + 1} ---")
        msg = connect_once()
        if msg:
            results.append(msg)
        time.sleep(DELAY)

    # Summary: show how connections were distributed across servers
    print("\n=== Summary ===")
    print(f"Total successful connections: {len(results)}")
    for msg in set(results):
        count = results.count(msg)
        print(f"  {msg}: {count} time(s)")


if __name__ == "__main__":
    main()
# I have input all of your code inside my environment.
# now please show me how to 
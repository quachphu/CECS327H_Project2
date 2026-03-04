"""
server.py - TCP Server for Anycast Simulation (Task 1)
CECS 327 - Project 2: A Bite of Distributed Communication

This server listens on port 5000 and responds with a unique identifier
message. Multiple instances of this server run behind Docker's built-in
DNS round-robin load balancing to simulate Anycast behavior, where a
client connects to one of several servers sharing the same hostname.

Environment Variable:
    SERVER_NAME: Unique name for this server instance (e.g., "server1")

How it works:
    1. Server binds to 0.0.0.0:5000 (all interfaces inside the container).
    2. Waits for incoming TCP connections.
    3. On connection, sends "Hello from <SERVER_NAME>" and closes.
    4. Logs all activity (ready, accepted, sent) to stdout.
"""

import socket
import os

# Read the server's unique name from an environment variable.
# Each container in docker-compose sets a different SERVER_NAME.
SERVER_NAME = os.environ.get("SERVER_NAME", "unknown_server")

# TCP socket configuration
HOST = "0.0.0.0"  # Listen on all network interfaces inside the container
PORT = 5000  # Common port shared by all anycast server instances


def main():
    """
    Main server loop:
    - Creates a TCP socket and binds it to HOST:PORT.
    - Listens for incoming connections one at a time.
    - Sends a greeting message identifying this specific server.
    """
    # Create a TCP/IPv4 socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow immediate port reuse after the server restarts.
    # Without this, the OS may keep the port in TIME_WAIT state.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the specified host and port
    server_socket.bind((HOST, PORT))

    # Start listening with a backlog queue of 5 pending connections
    server_socket.listen(5)
    print(f"Server ready on port {PORT}")

    # Infinite loop to accept and handle client connections
    while True:
        # accept() blocks until a client connects
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Build and send the unique greeting message
        message = f"Hello from {SERVER_NAME}"
        client_socket.sendall(message.encode("utf-8"))
        print(f"Sent: {message}")

        # Close the connection to this client
        client_socket.close()


if __name__ == "__main__":
    main()

"""
Resources used :
1. https://www.baeldung.com/cs/multicast-vs-broadcast-anycast-unicast?
2. https://www.youtube.com/watch?v=esLgiMLbRkI
3. https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client
4. https://stackoverflow.com/questions/72319941/what-do-socket-sol-socket-and-socket-so-reuseaddr-in-python
5. https://medium.com/uckey/the-behaviour-of-so-reuseport-addr-1-2-f8a440a35af6

"""

import socket
import os


SERVER_NAME = os.environ.get("SERVER_NAME", "unknown_server")

# TCP socket
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000  #  Assignment Required 5000 but can be any port not in use


def main():
    # Create a TCP/IPv4 socket
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # Using this resources : https://www.youtube.com/watch?v=esLgiMLbRkI

    # Allow immediate port reuse after the server restarts.( https://medium.com/uckey/the-behaviour-of-so-reuseport-addr-1-2-f8a440a35af6 )
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the specified host and port
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server ready on port {PORT}")

    while True:
        # accept() blocks until a client connects : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Build and send message
        message = f"Hello from {SERVER_NAME}"
        client_socket.sendall(message.encode("utf-8"))
        print(f"Sent: {message}")

        client_socket.close()  # Resources : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client


if __name__ == "__main__":
    main()

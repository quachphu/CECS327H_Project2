"""
Resources used :
1. https://www.baeldung.com/cs/multicast-vs-broadcast-anycast-unicast?
2. TCP vs UDP Sockets : https://www.youtube.com/watch?v=esLgiMLbRkI
3. https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

"""

import socket
import time

SERVER_HOST = "server"
SERVER_PORT = 5000

# Number of times the client will connect
NUM_ATTEMPTS = 6
DELAY = 1


def connect_once():
    """
    Opens a single TCP connection to the server service, receives message, prints it, and closes the connection.
    """
    try:
        # Create a new TCP socket, I using this resources : https://www.youtube.com/watch?v=esLgiMLbRkI
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        client_socket.connect(
            (SERVER_HOST, SERVER_PORT)
        )  # using this : https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

        # Receive up to 1024 bytes of data from the server : https://www.youtube.com/watch?v=esLgiMLbRkI
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
    # Runs multiple connection attempts to demonstrate Anycast
    print(f"Anycast client starting — will connect {NUM_ATTEMPTS} times\n")

    # Wait for servers ready on first run
    time.sleep(2)

    results = []
    for i in range(NUM_ATTEMPTS):
        print(f"Attempt {i + 1} ")
        msg = connect_once()
        if msg:
            results.append(msg)
        time.sleep(DELAY)


if __name__ == "__main__":
    main()

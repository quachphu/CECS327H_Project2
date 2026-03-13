"""
Resources :
1 https://www.youtube.com/watch?v=LnvxObLYO-o
2. https://pymotw.com/3/socket/multicast.html
3. https://pikotutorial.com/udp-multicasting-with-python/

"""

import socket
import struct
import json
import argparse
import time

# Multicast group configuration from assignment requirements
MULTICAST_GROUP = "224.1.1.1"
PORT = 5007
BUFFER_SIZE = 1024


def parse_args():
    parser = argparse.ArgumentParser(
        description="UDP Multicast Receiver joins a multicast group and displays received messages."
    )
    # resources : https://pikotutorial.com/udp-multicasting-with-python/
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Seconds to listen before leaving the group",
    )
    return parser.parse_args()


def handle_message(data, sender_address):
    print(f"Received: Multicast message from {sender_address}")

    # Attempt JSON decoding first
    try:
        message = json.loads(data.decode("utf-8"))
        print(f"Received: {json.dumps(message)}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If decoding fails, this is binary data
        print(f"Received: Binary data ({len(data)} bytes)")


def main():
    args = parse_args()
    duration = args.duration

    # Create a UDP socket, resources : https://www.youtube.com/watch?v=LnvxObLYO-o
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Resources : https://pymotw.com/3/socket/multicast.html
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to all server adresses.
    sock.bind(("", PORT))

    # Join the multicast group, resources : https://pymotw.com/3/socket/multicast.html
    membership_request = struct.pack(
        "4sL", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership_request)

    print("Joined multicast group")
    print(f"Listening on {MULTICAST_GROUP}:{PORT} for {duration} seconds\n")

    sock.settimeout(1.0)

    start_time = time.time()
    while (time.time() - start_time) < duration:
        try:
            data, sender_address = sock.recvfrom(BUFFER_SIZE)
            handle_message(data, sender_address)
        except socket.timeout:
            # if no data is received within the timeout, just check
            continue

    # Leave the multicast group by dropping membership, resources : https://pymotw.com/3/socket/multicast.html
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, membership_request)
    print("\nLeaving multicast group")

    sock.close()


if __name__ == "__main__":
    main()

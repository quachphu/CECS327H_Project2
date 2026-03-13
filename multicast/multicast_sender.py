"""
Resources :
1. https://www.youtube.com/watch?v=LnvxObLYO-o
2. https://pymotw.com/3/socket/multicast.html
3. https://pikotutorial.com/udp-multicasting-with-python/

"""

import socket
import struct
import json
import os
import time
import random


# Multicast group configuration from assignment requirements
MULTICAST_GROUP = "224.1.1.1"
PORT = 5007

# Multicast TTL: how many network hops the packet can traverse. Resources : https://pymotw.com/3/socket/multicast.html
MULTICAST_TTL = 2

# Second between messages and total messages to send before exiting
SEND_INTERVAL = 1
NUM_MESSAGES = 8
SENSOR_TYPE = os.environ.get("SENSOR_TYPE", "temp")


def create_json_message():
    """
    Build a JSON message.
    """
    if SENSOR_TYPE == "humidity":
        value = round(random.uniform(30.0, 90.0), 1)
    else:
        value = round(random.uniform(15.0, 35.0), 1)

    message = {"sensor": SENSOR_TYPE, "value": value}
    return json.dumps(message).encode("utf-8")


def create_binary_message():
    return os.urandom(16)  # used to simulate binary data sent over the network.


def main():
    # Create a UDP socket for sending multicast datagrams
    sock = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
    )  # resources : https://pikotutorial.com/udp-multicasting-with-python/
    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", MULTICAST_TTL)
    )  # resources :  https://pymotw.com/3/socket/multicast.html

    print(f"Multicast sender started (sensor: {SENSOR_TYPE})")
    print(f"Sending to {MULTICAST_GROUP}:{PORT} every {SEND_INTERVAL}s\n")
    time.sleep(3)

    for seq in range(1, NUM_MESSAGES + 1):
        # Alternate between JSON and binary messages
        if seq % 3 != 0:
            # Send JSON sensor reading
            data = create_json_message()
            sock.sendto(data, (MULTICAST_GROUP, PORT))
            print("Sent: Multicast message")
            print(f"Sent: {data.decode('utf-8')}")
        else:
            # Send binary data every 3rd message
            data = create_binary_message()
            sock.sendto(data, (MULTICAST_GROUP, PORT))
            print(f"Sent: Binary data ({len(data)} bytes)")

        time.sleep(SEND_INTERVAL)

    print("\nSender finished.")
    sock.close()


if __name__ == "__main__":
    main()

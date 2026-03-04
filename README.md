# CECS327H_Project2

# Project 2: A Bite of Distributed Communication

## CECS 327 – Intro to Networks and Distributed Computing

---

## Prerequisites

- Docker and Docker Compose installed
- Python 3.x (only needed if running scripts outside containers)
- tcpdump (installed inside containers for traffic monitoring)

---

## Task 1: Anycast with Docker (TCP)

### Build and Run

```bash
cd task1
docker-compose up --build
```

This launches **3 TCP server containers** (server1, server2, server3) and **1 client container**. All servers share the Docker DNS alias `server`, so the client's connections are distributed across them via round-robin — simulating Anycast.

### Re-run the Client

```bash
docker-compose run client
```

### Monitor Traffic with tcpdump

1. Find a running container ID:

   ```bash
   docker ps
   ```

2. Install tcpdump inside a server container:

   ```bash
   docker exec -it <container_id> apt-get update && apt-get install -y tcpdump
   ```

3. Capture TCP traffic on port 5000:
   ```bash
   docker exec -it <container_id> tcpdump -i eth0 tcp port 5000
   ```

### Expected Output

**Server logs (e.g., server1):**

```
Server ready on port 5000
Accepted connection from ('172.20.0.5', 48234)
Sent: Hello from server1
```

**Client output (multiple runs):**

```
Received: Hello from server1
Received: Hello from server3
Received: Hello from server2
```

### Clean Up

```bash
docker-compose down
```

---

## Task 2: Multicast with UDP

### Build and Run

```bash
cd task2
docker-compose up --build
```

This launches **2 senders** (temperature + humidity sensors) and **3 receivers** with different `--duration` values (40s, 25s, 15s). All receivers join multicast group `224.1.1.1:5007`.

### Monitor Traffic with tcpdump

1. Install tcpdump in a receiver container:

   ```bash
   docker exec -it <container_id> apt-get update && apt-get install -y tcpdump
   ```

2. Capture UDP multicast traffic:
   ```bash
   docker exec -it <container_id> tcpdump -i eth0 udp port 5007
   ```

### Expected Output

**Sender:**

```
Sent: Multicast message
Sent: {"sensor":"temp", "value":23.5, "seq":1}
```

**Receiver (15 seconds):**

```
Joined multicast group
Received: Multicast message from ('172.21.0.4', 5007)
Received: {"sensor": "temp", "value": 23.5, "seq": 1}
Leaving multicast group
```

**tcpdump:**

```
IP 172.21.0.4.56123 > 224.1.1.1.5007: UDP, length 32
```

### Observing Group Join/Leave Behavior

- receiver3 (15s) will leave the group first, missing later messages.
- receiver2 (25s) leaves next.
- receiver1 (40s) stays the longest, receiving the most data.
- Compare each receiver's output to see how join/leave timing affects delivery.

### Clean Up

```bash
docker-compose down
```

---

## Project Structure

```
project2/
├── README.md
├── task1/
│   ├── server.py              # TCP server (Anycast)
│   ├── client.py              # TCP client
│   ├── Dockerfile
│   └── docker-compose.yml
└── task2/
    ├── multicast_sender.py    # UDP multicast sender
    ├── multicast_receiver.py  # UDP multicast receiver
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Troubleshooting

- **Client can't connect:** Ensure all 3 servers are up before running the client. Use `docker-compose ps` to check.
- **No multicast messages received:** Docker's bridge network may filter multicast on some systems. Try `--network host` if needed.
- **tcpdump not found:** Install it with `apt-get update && apt-get install -y tcpdump` inside the container.

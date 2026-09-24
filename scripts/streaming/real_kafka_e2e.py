from confluent_kafka import Producer, Consumer
import json
import time
import uuid

BROKER = "localhost:9092"
TOPIC = "transactions.raw"
GROUP = f"sentinelx-e2e-{uuid.uuid4().hex[:8]}"

event_id = f"e2e-{uuid.uuid4().hex[:12]}"

event = {
    "event_id": event_id,
    "transaction_id": f"txn-{uuid.uuid4().hex[:12]}",
    "customer_id": "customer-e2e",
    "amount": 125.50,
    "currency": "USD",
    "timestamp": time.time(),
}

print("=== SENTINELX REAL KAFKA E2E ===")
print(f"Event: {event_id}")
print(f"Topic: {TOPIC}")
print(f"Group: {GROUP}")

producer = Producer({
    "bootstrap.servers": BROKER,
    "acks": "all",
    "message.timeout.ms": 10000,
})

delivery = []

def delivery_report(err, msg):
    delivery.append((err, msg))

producer.produce(
    TOPIC,
    key=event_id,
    value=json.dumps(event).encode("utf-8"),
    callback=delivery_report,
)

producer.flush(10)

if not delivery:
    raise RuntimeError("No Kafka delivery callback received")

err, msg = delivery[0]

if err:
    raise RuntimeError(f"Kafka delivery failed: {err}")

print(f"PRODUCED: partition={msg.partition()} offset={msg.offset()}")

consumer = Consumer({
    "bootstrap.servers": BROKER,
    "group.id": GROUP,
    "auto.offset.reset": "latest",
    "enable.auto.commit": False,
})

consumer.subscribe([TOPIC])

print("Waiting for consumed event...")

found = None
deadline = time.time() + 15

while time.time() < deadline:
    message = consumer.poll(1.0)

    if message is None:
        continue

    if message.error():
        raise RuntimeError(f"Kafka consumer error: {message.error()}")

    payload = json.loads(message.value().decode("utf-8"))

    if payload.get("event_id") == event_id:
        found = message
        print(
            f"CONSUMED: partition={message.partition()} "
            f"offset={message.offset()}"
        )
        print(f"PAYLOAD: {payload}")
        break

if found is None:
    consumer.close()
    raise RuntimeError("E2E event was not consumed")

consumer.commit(message=found, asynchronous=False)

committed = consumer.committed(
    [found.topic_partition()],
    timeout=10,
)[0]

print(
    f"COMMITTED: partition={committed.partition} "
    f"offset={committed.offset}"
)

if committed.offset < found.offset + 1:
    consumer.close()
    raise RuntimeError("Manual offset commit verification failed")

consumer.close()

print("")
print("===================================")
print("REAL KAFKA E2E: PASSED")
print("Producer -> Kafka -> Consumer -> Manual Commit")
print("===================================")

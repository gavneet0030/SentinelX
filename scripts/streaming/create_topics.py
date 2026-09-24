from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

BOOTSTRAP_SERVERS = "localhost:9092"

TOPICS = [
    "transactions.raw",
    "transactions.validated",
    "features.generated",
    "risk.decisions",
    "risk.alerts",
    "analyst.feedback",
    "transactions.dlq",
]


def create_topics():
    admin = AdminClient({
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "client.id": "sentinelx-topic-admin",
    })

    metadata = admin.list_topics(timeout=10)
    existing_topics = set(metadata.topics.keys())

    new_topics = [
        NewTopic(
            topic,
            num_partitions=3,
            replication_factor=1,
        )
        for topic in TOPICS
        if topic not in existing_topics
    ]

    if not new_topics:
        print("All SentinelX Kafka topics already exist.")
        return

    futures = admin.create_topics(new_topics)

    for topic, future in futures.items():
        try:
            future.result()
            print(f"Created topic: {topic}")
        except KafkaException as exc:
            print(f"Skipped topic {topic}: {exc}")

    print("\nSentinelX Kafka topics:")
    metadata = admin.list_topics(timeout=10)

    for topic in sorted(metadata.topics):
        if topic in TOPICS:
            print(f"  - {topic}")


if __name__ == "__main__":
    create_topics()

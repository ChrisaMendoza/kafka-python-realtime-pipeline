import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "logs-topic",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="python-consumers",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Consumer démarré. En attente de messages...")

for msg in consumer:
    data = msg.value
    print("Message reçu :", data)

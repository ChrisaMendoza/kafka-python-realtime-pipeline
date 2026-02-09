import os
import json
import uuid
from datetime import datetime
from kafka import KafkaProducer
from fake_data import generate_fake_request

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "logs-topic")

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

message = {
    "event_id": str(uuid.uuid4()),
    "timestamp": datetime.utcnow().isoformat(),
    "source": "python-producer",
    "type": "test",
    "payload": generate_fake_request()
}

producer.send(TOPIC, message)
producer.flush()

print(f"Message envoyé sur {TOPIC} via {BOOTSTRAP} :", message)
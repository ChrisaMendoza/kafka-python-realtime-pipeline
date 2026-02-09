import json
import uuid
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

message = {
    "event_id": str(uuid.uuid4()),
    "timestamp": datetime.utcnow().isoformat(),
    "source": "python-producer",
    "type": "test",
    "payload": {
        "message": "hello kafka"
    }
}

producer.send("logs-topic", message)
producer.flush()

print("Message envoyé :", message)

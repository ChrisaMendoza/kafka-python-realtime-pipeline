import json
import random
import time
import os
from datetime import datetime
from kafka import KafkaProducer

# Configuration du producteur Kafka
KAFKA_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Nom du topic Kafka
TOPIC_NAME = 'transactions'

# Liste de devises pour varier les données
DEVISES = ['EUR', 'USD', 'GBP', 'JPY', 'CHF']

def generer_transaction():
    """Génère une transaction financière factice"""
    transaction = {
        'id': f'TXN-{random.randint(10000, 99999)}',
        'montant': round(random.uniform(10.0, 5000.0), 2),
        'devise': random.choice(DEVISES),
        'timestamp': datetime.now().isoformat(),
        'type': random.choice(['debit', 'credit']),
        'merchant': random.choice(['Amazon', 'Apple Store', 'Restaurant Le Gourmet', 'Supermarché', 'Station Service'])
    }
    return transaction

def main():
    """Fonction principale qui envoie des transactions à Kafka"""
    print(f"🚀 Producteur Kafka démarré !")
    print(f"📤 Envoi de transactions vers le topic '{TOPIC_NAME}'...\n")
    
    try:
        compteur = 0
        while True:
            # Génère une transaction
            transaction = generer_transaction()
            
            # Envoie la transaction à Kafka
            producer.send(TOPIC_NAME, value=transaction)
            
            compteur += 1
            print(f"[{compteur}] ✅ Transaction envoyée : {transaction['id']} | "
                  f"{transaction['montant']} {transaction['devise']} | "
                  f"{transaction['type']} | {transaction['merchant']}")
            
            # Attend 2 secondes avant d'envoyer la prochaine transaction
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n⛔ Arrêt du producteur...")
    finally:
        producer.close()
        print("👋 Producteur fermé proprement.")

if __name__ == "__main__":
    main()
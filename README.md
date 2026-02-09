# Kafka Python Realtime Pipeline

Projet pédagogique de déploiement d'une application microservices avec :
- Python
- Kafka
- Docker
- Docker Compose
- Kubernetes
- CI/CD

## Objectif
Simuler un pipeline de données temps réel avec un producteur et un consommateur Kafka.

## Architecture
```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Producer    │─────▶│    Kafka     │─────▶│  Consumer    │
│   (Python)   │      │  + Zookeeper │      │   (Python)   │
└──────────────┘      └──────────────┘      └──────────────┘
```

## Prérequis
- Docker Desktop installé et démarré
- Git

## 🚀 Lancement avec Docker Compose

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/ChrisaMendoza/kafka-python-realtime-pipeline.git
cd kafka-python-realtime-pipeline
```

### 2️⃣ Lancer tous les services
```bash
docker-compose up --build
```

**Explication :**
- `--build` : Reconstruit les images Docker pour producer et consumer

### 3️⃣ Vérifier que ça fonctionne
Dans les logs, tu devrais voir :
- ✅ Zookeeper démarré
- ✅ Kafka démarré
- ✅ Producer envoie des transactions
- ✅ Consumer reçoit les transactions

### 4️⃣ Arrêter les services
```bash
Ctrl + C
```

Puis nettoyer :
```bash
docker-compose down
```

## 📦 Services Docker

| Service    | Port  | Description                           |
|------------|-------|---------------------------------------|
| Zookeeper  | 2181  | Coordination pour Kafka               |
| Kafka      | 9092  | Message broker                        |
| Producer   | -     | Envoie des transactions à Kafka       |
| Consumer   | -     | Consomme les transactions de Kafka    |

## 🛠️ Commandes utiles

### Voir les logs d'un service spécifique
```bash
docker-compose logs -f producer
docker-compose logs -f consumer
docker-compose logs -f kafka
```

### Redémarrer un service
```bash
docker-compose restart producer
```

### Voir les conteneurs en cours
```bash
docker ps
```

### Entrer dans un conteneur
```bash
docker exec -it kafka-producer bash
```

## 🔧 Variables d'environnement

Les services utilisent les variables suivantes :

**Producer et Consumer :**
- `KAFKA_BOOTSTRAP_SERVERS` : Adresse du serveur Kafka (définie dans docker-compose.yml)

## 📁 Structure du projet
```
.
├── docker-compose.yml       # Orchestration de tous les services
├── producer/
│   ├── app.py              # Script Python producteur
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image Docker du producteur
├── consumer/
│   ├── app.py              # Script Python consommateur
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image Docker du consommateur
└── README.md               # Ce fichier
```

## 👥 Équipe
- **Personne 1** : Chef de projet / Architecture
- **Personne 2** : Développement Python
- **Personne 3** : Docker
- **Personne 4** : Docker Compose
- **Personne 5** : Kubernetes et CI/CD

## 📝 Notes
Ce projet a été développé dans le cadre du TP "Déploiement d'Applications Microservices".
# 🚀 Pipeline de Données Temps Réel avec Kafka et Python

> Projet réalisé dans le cadre du TP "Containerisation et Orchestration" — M1 Data Engineering & Computer Science

---

## 📋 Description

Ce projet simule un **pipeline de données en temps réel** basé sur une architecture producteur/consommateur avec Apache Kafka. Un service Python génère des transactions financières fictives, les publie dans un topic Kafka, et un second service Python les consomme et les traite.

L'ensemble de l'application est conteneurisée avec Docker, orchestrable localement via Docker Compose, et déployable en production sur un cluster Kubernetes avec un pipeline CI/CD automatisé.

---

## 🏗️ Architecture

```
┌─────────────────┐       ┌───────────────────────────┐       ┌─────────────────┐
│                 │       │                           │       │                 │
│  Producer       │──────▶│  Kafka  +  Zookeeper      │──────▶│  Consumer       │
│  (Python)       │       │  (Message Broker)         │       │  (Python)       │
│                 │       │                           │       │                 │
└─────────────────┘       └───────────────────────────┘       └─────────────────┘
        │                             │                                │
        └─────────────────────────────┴────────────────────────────────┘
                                      │
                          Docker Compose / Kubernetes
```

**Flux de données :**
1. Le **Producer** génère des données de transactions fictives et les envoie dans le topic Kafka `transactions`
2. **Kafka** (avec Zookeeper pour la coordination) reçoit et stocke les messages
3. Le **Consumer** s'abonne au topic et traite les messages reçus en temps réel

---

## 📁 Structure du Projet

```
kafka-python-realtime-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # Pipeline GitHub Actions
│
├── producer/
│   ├── app.py                   # Script Python producteur (génération de transactions)
│   ├── requirements.txt         # Dépendances Python
│   └── Dockerfile               # Image Docker du producteur
│
├── consumer/
│   ├── app.py                   # Script Python consommateur
│   ├── requirements.txt         # Dépendances Python
│   └── Dockerfile               # Image Docker du consommateur
│
├── deploy/                      # Manifestes Kubernetes
│   ├── kafka-deployment.yaml
│   ├── zookeeper-deployment.yaml
│   ├── producer-deployment.yaml
│   ├── consumer-deployment.yaml
│   ├── configmap.yaml
│   └── secret.yaml
│
├── docker-compose.yml           # Orchestration locale de tous les services
├── .dockerignore                # Fichiers exclus du contexte de build
├── .gitignore                   # Fichiers exclus du dépôt Git
└── README.md
```

---

## 🛠️ Technologies Utilisées

| Technologie | Rôle |
|---|---|
| **Python 3.11** | Scripts producteur et consommateur |
| **Apache Kafka** | Message broker temps réel |
| **Zookeeper** | Coordination et gestion du cluster Kafka |
| **Docker** | Conteneurisation des services |
| **Docker Compose** | Orchestration locale multi-conteneurs |
| **Kubernetes** | Orchestration en production |
| **GitHub Actions** | Pipeline CI/CD |

---

## ⚙️ Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et démarré
- [Git](https://git-scm.com/)
- *(Pour Kubernetes)* [kubectl](https://kubernetes.io/docs/tasks/tools/) + [Minikube](https://minikube.sigs.k8s.io/) ou [kind](https://kind.sigs.k8s.io/)

---

## 🐳 Lancement avec Docker Compose (environnement local)

### 1. Cloner le projet

```bash
git clone https://github.com/ChrisaMendoza/kafka-python-realtime-pipeline.git
cd kafka-python-realtime-pipeline
```

### 2. Lancer tous les services

```bash
docker-compose up --build
```

> Le flag `--build` force la reconstruction des images Docker du producer et du consumer.

### 3. Vérifier le bon fonctionnement

Dans les logs de la console, vous devriez observer :

```
zookeeper  | ... Started
kafka      | ... [KafkaServer id=1] started
producer   | ✅ Transaction envoyée : {"id": "txn-001", "montant": 142.50, ...}
consumer   | ✅ Message reçu : {"id": "txn-001", "montant": 142.50, ...}
```

### 4. Arrêter et nettoyer

```bash
# Arrêter les services (Ctrl+C puis)
docker-compose down

# Supprimer également les volumes
docker-compose down -v
```

---

## 🔍 Commandes Utiles

```bash
# Voir les logs en direct d'un service
docker-compose logs -f producer
docker-compose logs -f consumer
docker-compose logs -f kafka

# Redémarrer un service spécifique
docker-compose restart producer

# Lister les conteneurs actifs
docker ps

# Entrer dans un conteneur
docker exec -it kafka-producer bash
```

---

## ☸️ Déploiement sur Kubernetes

### Prérequis

Assurez-vous que votre cluster est actif :

```bash
minikube start
# ou
kind create cluster
```

### Appliquer les manifestes

```bash
kubectl apply -f deploy/
```

### Vérifier le déploiement

```bash
# Lister les pods
kubectl get pods

# Lister les services
kubectl get svc

# Lister les déploiements
kubectl get deployments

# Voir les logs d'un pod
kubectl logs -f <nom-du-pod>
```

### Démonstration de l'auto-réparation (self-healing)

Kubernetes redémarre automatiquement les pods défaillants. Pour le vérifier :

```bash
# Supprimer un pod manuellement
kubectl delete pod <nom-du-pod-producer>

# Observer le redémarrage automatique
kubectl get pods -w
```

---

## 🔧 Variables d'Environnement

Les services utilisent les variables suivantes, définies dans `docker-compose.yml` et gérées via `ConfigMap` / `Secret` dans Kubernetes :

| Variable | Description | Valeur par défaut |
|---|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | Adresse du broker Kafka | `kafka:9092` |
| `KAFKA_TOPIC` | Nom du topic Kafka | `transactions` |

> ⚠️ Aucun secret n'est stocké en clair dans le dépôt Git ni dans les images Docker.

---

## 🔄 Pipeline CI/CD

Le pipeline GitHub Actions (`.github/workflows/ci-cd.yml`) s'exécute automatiquement selon les règles suivantes :

| Déclencheur | Action |
|---|---|
| Push sur `develop` | Build des images Docker + tests |
| Création d'un tag Git sur `main` | Build + Push vers le registre + Déploiement sur Kubernetes |

**Étapes du pipeline :**
1. 🔨 **Build** — Construction des images Docker (`producer`, `consumer`)
2. 📦 **Push** — Publication des images vers le registre Docker Hub / GHCR
3. 🚀 **Deploy** — Application des manifestes Kubernetes (`kubectl apply`)

---

## 📊 Services et Ports

| Service | Port exposé | Description |
|---|---|---|
| Zookeeper | `2181` | Coordination du cluster Kafka |
| Kafka | `9092` | Message broker principal |
| Producer | — | Service interne, sans port exposé |
| Consumer | — | Service interne, sans port exposé |

---

## 👥 Équipe

| Membre | Rôle |
|---|---|
| **Chrisa** | Chef de projet, Architecture, Documentation |
| **Flavie** | Développement Python (Producer & Consumer) |
| **Ekta** | Conteneurisation Docker (Dockerfiles) |
| **Léora** | Orchestration Docker Compose |
| **Angelikia** | Kubernetes & Pipeline CI/CD |

---

## 🤖 Utilisation de l'IA

Conformément aux consignes du TP, des outils d'IA (Claude, ChatGPT) ont été utilisés ponctuellement pour :
- La génération de gabarits de code Dockerfile et de manifestes Kubernetes
- La rédaction de ce README

Tout le code généré a été relu, compris, testé et adapté par chaque membre de l'équipe.

---

## 📈 Axes d'Amélioration

- **Monitoring** : Intégration de Prometheus + Grafana pour visualiser les métriques (nombre de messages/s, latence)
- **Logging centralisé** : Déploiement d'une stack Loki + Promtail pour agréger les logs de tous les services
- **Sécurité** : Scan des images Docker avec Trivy dans le pipeline CI/CD
- **Gestion des dépendances** : Migration vers [uv](https://github.com/astral-sh/uv) comme gestionnaire de dépendances Python

---

## 📝 Informations Projet

Ce projet a été réalisé dans le cadre du cours **"Containerisation et Orchestration"** — M1 Data Engineering & Computer Science.

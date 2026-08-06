# Monitoring & Dérive de Modèles — MLOps

## Description

Ce projet implémente une solution de monitoring continu pour détecter et visualiser la dérive (drift) d'un modèle de machine learning en production. Il répond à la problématique suivante : *comment instrumenter un pipeline MLOps pour détecter automatiquement une dégradation des performances (Concept Drift) ou un changement dans les caractéristiques d'entrée (Data Drift) avant que le modèle ne devienne obsolète ?*

Le projet simule un modèle de prédiction du prix de logements (dataset California Housing) mis en production, dont les données d'entrée dérivent progressivement dans le temps. Il détecte cette dérive, l'expose sous forme de métriques, la visualise dans un dashboard, et déclenche une alerte automatique en cas de dépassement de seuil.

## Architecture

```
Données (California Housing)
      │
      ▼
Entraînement du modèle (RandomForest)
      │
      ▼
Simulation de dérive (Data Drift + Concept Drift)
      │
      ▼
Détection de dérive (Evidently AI)
      │
      ▼
Export des métriques (prometheus_client)
      │
      ▼
Stockage des métriques (Prometheus)
      │
      ▼
Visualisation (Grafana) ──► Alerte automatique (webhook)
```

Le tout tourne dans 3 conteneurs Docker orchestrés par `docker-compose` :
- **python-app** : exécute le pipeline (préparation des données → entraînement → simulation de drift → détection → export des métriques)
- **prometheus** : stocke les métriques de drift dans le temps
- **grafana** : affiche les dashboards et gère l'alerting

## Technologies

- **Python 3.10**
- **Evidently AI** — détection de dérive (data drift, scores statistiques par feature)
- **scikit-learn** — entraînement du modèle (RandomForestRegressor)
- **Prometheus** — stockage des métriques (time series)
- **Grafana** — dashboarding et alerting
- **Docker / Docker Compose** — conteneurisation

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé
- Git

## Installation et lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/Mountata/Monitoring-D-rive-de-mod-les.git
cd Monitoring-D-rive-de-mod-les
```

### 2. Construire les images Docker

```bash
docker-compose build
```

⚠️ Cette étape peut prendre plusieurs minutes la première fois (installation des dépendances Python : scikit-learn, evidently, etc.).

### 3. Lancer tous les services

```bash
docker-compose up -d
```

Cette commande démarre les 3 conteneurs. Le conteneur `python-app` exécute automatiquement le pipeline complet (préparation des données, entraînement, simulation de drift, détection) puis lance le serveur d'export de métriques, qui reste actif en continu.

### 4. Vérifier que tout fonctionne

```bash
docker ps
```

Tu dois voir 3 conteneurs avec le statut `Up` : `mlops-drift-monitoring` (ou `python-app`), `prometheus`, `grafana`.

## Accès aux interfaces

| Service | URL | Identifiants |
|---|---|---|
| Métriques brutes (Prometheus format) | http://localhost:8000/metrics | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | `admin` / `admin` |

Dans Grafana, le dashboard **"Monitoring_dashboard"** est accessible depuis le menu **Dashboards**. Il contient 4 panels :
- **Nombre de dérives actives** (jauge)
- **Scores de drift par feature** (bar chart)
- **Évolution des scores de drift** (time series)
- **Alertes de drift** (tableau)

Une règle d'alerte Grafana (**Alerting > Alert rules**) se déclenche automatiquement lorsque plus de 2 features sont en dérive simultanément.

## Structure du projet

```
.
├── .docker/
│   ├── prometheus/
│   │   └── prometheus.yml          # Configuration du scraping Prometheus
│   └── grafana/
│       └── provisioning/
│           ├── datasources/        # Connexion auto Grafana → Prometheus
│           └── dashboards/         # Chargement auto des dashboards
├── data/
│   ├── raw/                        # Dataset complet
│   ├── reference/                  # Données de référence (entraînement)
│   └── production/                 # Données de production (V1 propre, V2 avec drift)
├── models/                         # Modèle entraîné (model_v1.pkl)
├── reports/                        # Rapport HTML Evidently + scores JSON
├── src/
│   ├── prepare_data_01.py          # Chargement et split du dataset
│   ├── train_model_02.py           # Entraînement du modèle
│   ├── simulate_drift_03.py        # Génération de données avec dérive simulée
│   ├── detect_drift_04.py          # Détection de drift avec Evidently AI
│   ├── export_metrics_05.py        # Serveur d'export Prometheus
│   └── pipeline_full_06.py         # Orchestration complète (01→04 puis serveur 05)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt                # Dépendances figées (pip freeze)
```

## Relancer uniquement le pipeline (sans redémarrer les conteneurs)

```bash
docker-compose run --rm python-app python src/pipeline_full_06.py
```

## Arrêter le projet

```bash
docker-compose down
```

Pour tout supprimer, y compris les volumes de données Prometheus/Grafana :

```bash
docker-compose down -v
```

## Développement local (optionnel)

Pour itérer rapidement sur les scripts sans passer par Docker à chaque test :

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements-local.txt
python src/prepare_data_01.py
```

`requirements-local.txt` exclut les dépendances incompatibles avec Windows (ex: `uvloop`), non utilisées par les scripts du pipeline.

## Auteurs

Projet réalisé dans le cadre du sujet *Monitoring & Dérive de modèles (Data & Concept Drift)*.
FROM python:3.10-slim

# Éviter les questions interactives
ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY src/ ./src/
COPY data/ ./data/
COPY models/ ./models/

# Port pour l'export Prometheus
EXPOSE 8000

# Commande par défaut
CMD ["python", "-m", "src.06_pipeline_full"]
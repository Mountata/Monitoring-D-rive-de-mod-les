"""
Script 05 : Export des métriques vers Prometheus
- Expose les métriques de drift via un serveur HTTP
"""
from prometheus_client import Gauge, start_http_server
import time
import json
import os
import threading

drift_score_gauge = Gauge('drift_score', 'Drift score per feature', ['feature'])
drift_detected_gauge = Gauge('drift_detected', 'Boolean indicating drift (1) or not (0)', ['feature'])
alert_count_gauge = Gauge('drift_alerts_count', 'Number of features currently drifting')


def update_metrics():
    while True:
        try:
            if os.path.exists('reports/drift_scores.json'):
                with open('reports/drift_scores.json', 'r') as f:
                    drift_scores = json.load(f)

                alert_count = 0
                for feature, score in drift_scores.items():
                    drift_score_gauge.labels(feature=feature).set(score)
                    is_drift = 1 if score > 0.3 else 0
                    drift_detected_gauge.labels(feature=feature).set(is_drift)
                    if is_drift:
                        alert_count += 1
                alert_count_gauge.set(alert_count)
                print(f"✅ Métriques mises à jour - {len(drift_scores)} features, {alert_count} alertes")
        except Exception as e:
            print(f"⚠️ Erreur de mise à jour : {e}")

        time.sleep(10)  # relit le fichier toutes les 10 secondes


def start_metrics_server(port=8000):
    print("=" * 60)
    print("ÉTAPE 5 : EXPORT VERS PROMETHEUS")
    print("=" * 60)

    print(f"\n[1] Démarrage du serveur sur le port {port}...")
    start_http_server(port)
    print(f"    - Métriques disponibles sur http://localhost:{port}/metrics")

    print("\n[2] Lancement du thread de mise à jour...")
    thread = threading.Thread(target=update_metrics, daemon=True)
    thread.start()

    print("\n[3] SERVEUR EN EXÉCUTION (Ctrl+C pour arrêter)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du serveur...")


if __name__ == "__main__":
    start_metrics_server(8000)
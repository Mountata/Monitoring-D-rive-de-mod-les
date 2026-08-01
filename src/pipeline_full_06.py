"""
Script 06 : Pipeline complet
- Exécute les étapes 01 à 04 dans l'ordre
- Lance ensuite le serveur de métriques Prometheus (reste actif)
"""
import os
import subprocess
import time

STEPS = [
    ("prepare_data_01.py", "PRÉPARATION DES DONNÉES"),
    ("train_model_02.py", "ENTRAÎNEMENT DU MODÈLE"),
    ("simulate_drift_03.py", "SIMULATION DE DÉRIVE"),
    ("detect_drift_04.py", "DÉTECTION DE DÉRIVE"),
]


def run_pipeline():
    print("=" * 60)
    print("🚀 PIPELINE COMPLET - MONITORING MLOPS")
    print("=" * 60)

    for script, name in STEPS:
        print(f"\n{'='*60}\n▶️  ÉTAPE : {name}\n{'='*60}")
        script_path = os.path.join('src', script)

        try:
            result = subprocess.run(
                ['python', script_path], check=True, capture_output=True, text=True
            )
            print(result.stdout)
            if result.stderr:
                print(f"⚠️ Avertissements :\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'exécution de {script}")
            print(e.stderr)
            return False

        time.sleep(1)

    report_path = 'reports/drift_report.html'
    if os.path.exists(report_path):
        print(f"\n✅ Rapport généré : {report_path}")

    print("\n" + "=" * 60)
    print("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 60)

    return True


def start_monitoring_server():
    print("\n" + "=" * 60)
    print("📡 DÉMARRAGE DU SERVEUR DE MÉTRIQUES")
    print("=" * 60)
    print("Le conteneur reste actif pour exposer les métriques à Prometheus.")
    print("Endpoint : http://python-app:8000/metrics\n")

    # Ce subprocess bloque volontairement (le serveur tourne en boucle infinie)
    subprocess.run(['python', 'src/export_metrics_05.py'])


if __name__ == "__main__":
    success = run_pipeline()
    if success:
        start_monitoring_server()
    else:
        print("\n❌ Le pipeline a échoué, le serveur de métriques n'est pas démarré.")
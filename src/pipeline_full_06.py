"""
Script 06 : Pipeline complet
- Exécute les étapes 01 à 04 dans l'ordre
"""
import os
import subprocess
import webbrowser
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
    print("\n🔍 Prochaine étape : lancer l'export Prometheus avec")
    print("   python src/export_metrics_05.py")

    return True


if __name__ == "__main__":
    run_pipeline()
"""
Script 04 : Détection de dérive avec Evidently AI
- Compare données de référence et de production
- Calcule les métriques de drift
- Génère un rapport HTML
"""
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently import ColumnMapping
import os
import json


def detect_drift():
    print("=" * 60)
    print("ÉTAPE 4 : DÉTECTION DE DÉRIVE")
    print("=" * 60)

    # 1. Charger les données
    print("\n[1] Chargement des données...")
    ref_df = pd.read_csv('data/reference/reference_data.csv')
    prod_df = pd.read_csv('data/production/production_data_v2.csv')

    # 2. Configuration Evidently
    print("\n[2] Configuration d'Evidently...")
    column_mapping = ColumnMapping()
    column_mapping.target = 'MedHouseVal'

    # 3. Génération du rapport
    print("\n[3] Création du rapport de drift...")
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_df, current_data=prod_df, column_mapping=column_mapping)

    # 4. Sauvegarde HTML
    print("\n[4] Sauvegarde du rapport...")
    os.makedirs('reports', exist_ok=True)
    report.save_html('reports/drift_report.html')
    print("    - reports/drift_report.html")

    # 5. Extraction des scores
    print("\n[5] Extraction des métriques de drift...")
    report_dict = report.as_dict()
    drift_scores = {}

    try:
        for metric in report_dict.get('metrics', []):
            if metric.get('metric') == 'DataDriftTable':
                columns = metric.get('result', {}).get('drift_by_columns', {})
                for col_name, col_data in columns.items():
                    drift_scores[col_name] = col_data.get('drift_score', 0)
    except Exception as e:
        print(f"    - Extraction impossible : {e}")

    if not drift_scores:
        print("    - Aucun score extrait automatiquement, vérifier la version d'Evidently installée")

    # 6. Sauvegarde des scores pour Prometheus
    with open('reports/drift_scores.json', 'w') as f:
        json.dump(drift_scores, f)

    # 7. Affichage
    print("\n[6] RÉSULTATS :")
    alert_features = []
    for feature, score in sorted(drift_scores.items(), key=lambda x: x[1], reverse=True):
        status = "🔴 DRIFT" if score > 0.3 else "🟡 WARNING" if score > 0.15 else "🟢 OK"
        print(f"        {feature} : {score:.3f} → {status}")
        if score > 0.3:
            alert_features.append(feature)

    print("\n[7] ALERTES :")
    if alert_features:
        print(f"    ⚠️ Dérive détectée sur : {', '.join(alert_features)}")
    else:
        print("    ✅ Aucune dérive critique détectée")

    return drift_scores, alert_features


if __name__ == "__main__":
    detect_drift()
    print("\n✅ ÉTAPE 4 TERMINÉE")
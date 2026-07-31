"""
Script 04 : Détection de dérive avec Evidently AI
- Compare données de référence et de production
- Calcule les métriques de drift
- Génère un rapport HTML

Migré vers la nouvelle API Evidently (>= 0.7.x).
Ancienne API (evidently.report.Report / evidently.metric_preset) supprimée
depuis Evidently 0.7 ; cette version utilise :
    from evidently import Report, Dataset, DataDefinition
    from evidently.presets import DataDriftPreset
    from evidently.metrics import ValueDrift
"""
import os
import re
import json

import pandas as pd
from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset
from evidently.metrics import ValueDrift


def detect_drift():
    print("=" * 60)
    print("ÉTAPE 4 : DÉTECTION DE DÉRIVE")
    print("=" * 60)

    # 1. Charger les données
    print("\n[1] Chargement des données...")
    ref_df = pd.read_csv('data/reference/reference_data.csv')
    prod_df = pd.read_csv('data/production/production_data_v2.csv')

    # 2. Configuration Evidently (nouvelle API : Dataset + DataDefinition
    #    remplacent ColumnMapping)
    print("\n[2] Configuration d'Evidently...")
    target_column = 'MedHouseVal'
    feature_columns = [c for c in ref_df.columns if c != target_column]

    data_definition = DataDefinition()
    ref_dataset = Dataset.from_pandas(ref_df, data_definition=data_definition)
    prod_dataset = Dataset.from_pandas(prod_df, data_definition=data_definition)

    # 3. Génération du rapport
    #    - DataDriftPreset() pour la vue d'ensemble (utilisée dans le HTML)
    #    - ValueDrift(column=...) par colonne pour une extraction fiable
    #      des scores individuels (target inclus, comme dans l'ancien script)
    print("\n[3] Création du rapport de drift...")
    all_columns = feature_columns + [target_column]
    report = Report(
        metrics=[DataDriftPreset()] + [ValueDrift(column=col) for col in all_columns]
    )
    my_eval = report.run(current_data=prod_dataset, reference_data=ref_dataset)

    # 4. Sauvegarde HTML (méthode portée par le résultat du run, pas par Report)
    print("\n[4] Sauvegarde du rapport...")
    os.makedirs('reports', exist_ok=True)
    my_eval.save_html('reports/drift_report.html')
    print("    - reports/drift_report.html")

    # 5. Extraction des scores
    print("\n[5] Extraction des métriques de drift...")
    result_dict = my_eval.dict()
    drift_scores = {}

    try:
        for metric in result_dict.get('metrics', []):
            metric_id = metric.get('metric_id', '')
            match = re.search(r'ValueDrift\(column=([^,)]+)', metric_id)
            if match:
                col_name = match.group(1)
                drift_scores[col_name] = metric.get('value', 0)
    except Exception as e:
        print(f"    - Extraction impossible : {e}")

    if not drift_scores:
        print("    - Aucun score extrait automatiquement, vérifier la structure de my_eval.dict()")
        print(json.dumps(result_dict, indent=2, default=str)[:2000])

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
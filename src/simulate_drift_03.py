"""
Script 03 : Simulation de dérive
- Crée des données de production avec biais
- Simule Data Drift et Concept Drift
"""
import pandas as pd
import numpy as np


def simulate_drift():
    print("=" * 60)
    print("ÉTAPE 3 : SIMULATION DE DÉRIVE")
    print("=" * 60)

    # 1. Charger les données de production V1 (non biaisées)
    print("\n[1] Chargement des données de production V1...")
    df = pd.read_csv('data/production/production_data_v1.csv')
    df_v2 = df.copy()

    # 2. Appliquer les dérives
    print("\n[2] Application des dérives...")

    # Data Drift : le revenu médian augmente de 20%
    df_v2['MedInc'] = df_v2['MedInc'] * 1.2
    print("    - MedInc × 1.2 (Data Drift)")

    # Data Drift : le nombre moyen de pièces diminue de 30%
    df_v2['AveRooms'] = df_v2['AveRooms'] * 0.7
    print("    - AveRooms × 0.7 (Data Drift)")

    # Concept Drift : la relation entre les features et le prix change
    df_v2['MedHouseVal'] = df_v2['MedHouseVal'] * 1.3
    print("    - MedHouseVal × 1.3 (Concept Drift)")

    # Bruit aléatoire sur l'âge des logements
    noise = np.random.normal(0, df['HouseAge'].std() * 0.1, len(df))
    df_v2['HouseAge'] = df_v2['HouseAge'] + noise
    print("    - HouseAge + bruit (10%)")

    # 3. Sauvegarde
    print("\n[3] Sauvegarde des données de production V2...")
    df_v2.to_csv('data/production/production_data_v2.csv', index=False)
    print("    - data/production/production_data_v2.csv")

    return df_v2


if __name__ == "__main__":
    simulate_drift()
    print("\n✅ ÉTAPE 3 TERMINÉE")
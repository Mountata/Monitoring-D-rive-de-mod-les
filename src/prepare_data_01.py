"""
Script 01 : Préparation des données
- Charge le dataset California Housing
- Divise en train/test
- Sauvegarde les données de référence
"""
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import os


def prepare_data():
    print("=" * 60)
    print("ÉTAPE 1 : PRÉPARATION DES DONNÉES")
    print("=" * 60)

    # 1. Charger le dataset
    print("\n[1] Chargement du dataset California Housing...")
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['MedHouseVal'] = housing.target

    print(f"    - Lignes : {len(df)}")
    print(f"    - Colonnes : {list(df.columns)}")

    # 2. Split train/test
    print("\n[2] Division en train/test...")
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)
    print(f"    - Train : {len(train_df)} lignes")
    print(f"    - Test  : {len(test_df)} lignes")

    # 3. Sauvegarde
    print("\n[3] Sauvegarde des données...")
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/reference', exist_ok=True)
    os.makedirs('data/production', exist_ok=True)

    df.to_csv('data/raw/housing.csv', index=False)
    train_df.to_csv('data/reference/reference_data.csv', index=False)
    test_df.to_csv('data/production/production_data_v1.csv', index=False)

    print("    - data/raw/housing.csv")
    print("    - data/reference/reference_data.csv")
    print("    - data/production/production_data_v1.csv")

    return train_df, test_df, df


if __name__ == "__main__":
    prepare_data()
    print("\n✅ ÉTAPE 1 TERMINÉE")
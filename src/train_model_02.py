"""
Script 02 : Entraînement du modèle
- Entraîne un RandomForestRegressor
- Évalue les performances
- Sauvegarde le modèle
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os


def train_model():
    print("=" * 60)
    print("ÉTAPE 2 : ENTRAÎNEMENT DU MODÈLE")
    print("=" * 60)

    # 1. Charger les données de référence
    print("\n[1] Chargement des données de référence...")
    df = pd.read_csv('data/reference/reference_data.csv')
    X = df.drop('MedHouseVal', axis=1)
    y = df['MedHouseVal']

    # 2. Entraînement
    print("\n[2] Entraînement du modèle RandomForest...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X, y)
    print("    - Modèle entraîné avec succès")

    # 3. Évaluation sur les données de test (production V1)
    print("\n[3] Évaluation sur les données de test...")
    test_df = pd.read_csv('data/production/production_data_v1.csv')
    X_test = test_df.drop('MedHouseVal', axis=1)
    y_test = test_df['MedHouseVal']

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"    - RMSE : {rmse:.4f}")
    print(f"    - R²   : {r2:.4f}")

    # 4. Sauvegarde du modèle
    print("\n[4] Sauvegarde du modèle...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model_v1.pkl')
    print("    - models/model_v1.pkl")

    return model, rmse, r2


if __name__ == "__main__":
    train_model()
    print("\n✅ ÉTAPE 2 TERMINÉE")
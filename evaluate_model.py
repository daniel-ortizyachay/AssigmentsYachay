import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle

def evaluate_model(data_file, user_factors_file, movie_factors_file):
    # Cargar datos de prueba
    df = pd.read_csv(data_file)
    df = df[['userId', 'movieId', 'rating']]

    # Cargar factores de usuario y película
    with open(user_factors_file, "rb") as f:
        user_factors = pickle.load(f)
    with open(movie_factors_file, "rb") as f:
        movie_factors = pickle.load(f)

    # Predicciones y calificaciones reales
    predictions = []
    actuals = []
    for _, row in df.iterrows():
        user_id = int(row['userId']) - 1  # Ajustar índice (0 basado)
        movie_id = int(row['movieId']) - 1  # Ajustar índice (0 basado)
        actual_rating = row['rating']

        # Verificar si el usuario y la película están en los factores
        if user_id < len(user_factors) and movie_id < len(movie_factors):
            predicted_rating = np.dot(user_factors[user_id], movie_factors[movie_id])
            predictions.append(predicted_rating)
            actuals.append(actual_rating)

    # Calcular RMSE
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    print(f"Offline RMSE: {rmse}")

# Configuración
evaluate_model("ml-latest-small/ratings.csv", "user_factors.pkl", "movie_factors.pkl")
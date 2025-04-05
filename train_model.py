import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

def train_model(data_file, model_file):
    # Cargar datos de MovieLens Small Dataset
    df = pd.read_csv(data_file)
    df = df[['userId', 'movieId', 'rating']]  # Asegurarse de usar solo las columnas necesarias

    # Crear una matriz de usuario-película
    user_movie_matrix = df.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    # Factorización de matrices con TruncatedSVD
    svd = TruncatedSVD(n_components=20, random_state=42)
    user_factors = svd.fit_transform(user_movie_matrix)  # Factores de usuario
    movie_factors = svd.components_.T  # Factores de película

    # Guardar el modelo y los factores
    with open(model_file, 'wb') as f:
        pickle.dump(svd, f)
    with open("user_factors.pkl", "wb") as f:
        pickle.dump(user_factors, f)
    with open("movie_factors.pkl", "wb") as f:
        pickle.dump(movie_factors, f)

    print(f"Model and factors saved successfully.")

# Configuración
train_model("ml-latest-small/ratings.csv", "recommendation_model.pkl")
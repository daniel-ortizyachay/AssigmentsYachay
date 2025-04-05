from flask import Flask, jsonify
import pickle
import time
from confluent_kafka import Producer
import numpy as np
import csv
import os
import pandas as pd
import random

app = Flask(__name__)

# Cargar el modelo entrenado y los factores
with open("recommendation_model.pkl", "rb") as f:
    svd = pickle.load(f)

# Cargar la matriz de factores de usuario y película
with open("user_factors.pkl", "rb") as f:
    user_factors = pickle.load(f)

with open("movie_factors.pkl", "rb") as f:
    movie_factors = pickle.load(f)

# Cargar información de películas
movies = pd.read_csv("ml-latest-small/movies.csv").set_index("movieId")

# Configurar el productor de Kafka
producer = Producer({'bootstrap.servers': '172.23.224.1:9092'})

# Asegúrate de que el archivo recommendation_data.csv exista y tenga encabezados
if not os.path.exists("recommendation_data.csv"):
    with open("recommendation_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "movie_id", "score", "genre", "region", "response_time"])  # Encabezados

def validate_data(file_path):
    df = pd.read_csv(file_path)
    required_columns = ["user_id", "movie_id", "score", "response_time"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("El archivo no contiene todas las columnas requeridas.")
    print("Los datos son válidos.")

validate_data("recommendation_data.csv")

# Lista de regiones ficticias
regions = ["North America", "Europe", "Asia", "South America", "Africa"]

# Función para asignar regiones aleatorias
def get_random_region(user_id):
    random.seed(user_id)  # Asegurar consistencia
    return random.choice(regions)

def log_to_kafka(user_id, recommendations, response_time, status):
    """Enviar logs al stream de Kafka."""
    log_message = f"{int(time.time())},{user_id},recommendation request server,status {status},result: {','.join(map(str, recommendations))},responsetime {response_time}ms"
    producer.produce("movielog1", log_message)
    producer.flush()

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    start_time = time.time()  # Registrar el tiempo de inicio

    try:
        # Verificar si el usuario existe en los factores
        if user_id >= len(user_factors):
            raise ValueError(f"User ID {user_id} not found in user factors.")

        # Generar recomendaciones para el usuario
        user_vector = user_factors[user_id]
        scores = np.dot(movie_factors, user_vector)  # Producto punto con todos los factores de película
        movie_ids = np.argsort(scores)[::-1][:20]  # Obtener los 20 mejores índices (películas)

        # Calcular el tiempo de respuesta
        response_time = int((time.time() - start_time) * 1000)

        # Guardar las recomendaciones en recommendation_data.csv
        with open("recommendation_data.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for movie_id, score in zip(movie_ids, scores[movie_ids]):
                genre = movies.loc[movie_id, "genres"] if movie_id in movies.index else "Unknown"
                region = get_random_region(user_id)
                writer.writerow([user_id, movie_id, score, genre, region, response_time])

        # Log exitoso a Kafka
        log_to_kafka(user_id, movie_ids.tolist(), response_time, 200)

        # Responder con las recomendaciones
        return jsonify({"user_id": user_id, "recommendations": movie_ids.tolist()}), 200

    except Exception as e:
        # En caso de error, log a Kafka
        response_time = int((time.time() - start_time) * 1000)
        log_to_kafka(user_id, [], response_time, 500)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
import pandas as pd

def evaluate_fairness(data_file):
    df = pd.read_csv(data_file)

    # Calcular calificación promedio por región
    region_avg = df.groupby("region")["score"].mean()
    print("Calificación promedio por región:")
    print(region_avg)

    # Verificar diversidad de géneros en recomendaciones
    genre_counts = df["genre"].value_counts(normalize=True)
    print("Distribución de géneros en recomendaciones:")
    print(genre_counts)

# Configuración
evaluate_fairness("recommendation_data.csv")
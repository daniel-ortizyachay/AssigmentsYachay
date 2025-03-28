import pandas as pd

def validate_schema(data_file):
    expected_columns = ["userId", "movieId", "rating"]
    df = pd.read_csv(data_file)

    # Verificar columnas
    if list(df.columns) != expected_columns:
        raise ValueError(f"Esquema inválido. Se esperaban columnas: {expected_columns}")

    print("Esquema válido.")

def detect_drift(current_file, reference_file):
    current_df = pd.read_csv(current_file)
    reference_df = pd.read_csv(reference_file)

    # Comparar estadísticas
    for column in ["rating"]:
        current_mean = current_df[column].mean()
        reference_mean = reference_df[column].mean()
        if abs(current_mean - reference_mean) > 0.1:  # Umbral de drift
            print(f"Drift detectado en {column}: {current_mean} vs {reference_mean}")

# Configuración
validate_schema("ml-latest-small/ratings.csv")
detect_drift("ml-latest-small/ratings.csv", "reference_data.csv")
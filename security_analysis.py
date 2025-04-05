import pandas as pd

def analyze_data_poisoning(data_file):
    df = pd.read_csv(data_file)

    # Detectar usuarios con patrones de calificación sospechosos
    suspicious_users = df.groupby("user_id")["score"].std().sort_values()
    print("Usuarios con patrones de calificación sospechosos:")
    print(suspicious_users.head(10))

# Configuración
analyze_data_poisoning("recommendation_data.csv")
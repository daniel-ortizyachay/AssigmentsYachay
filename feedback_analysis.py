import pandas as pd

def analyze_feedback_loop(data_file):
    df = pd.read_csv(data_file)

    # Analizar si las películas populares reciben más calificaciones
    popular_movies = df.groupby("movie_id")["score"].count().sort_values(ascending=False)
    print("Películas más calificadas:")
    print(popular_movies.head(10))

    # Analizar diversidad de recomendaciones para usuarios con pocas interacciones
    user_interactions = df.groupby("user_id")["movie_id"].count()
    low_interaction_users = user_interactions[user_interactions < 5].index
    recommendations = df[df["user_id"].isin(low_interaction_users)]
    genre_diversity = recommendations["genre"].value_counts(normalize=True)
    print("Diversidad de géneros para usuarios con pocas interacciones:")
    print(genre_diversity)

# Configuración
analyze_feedback_loop("recommendation_data.csv")
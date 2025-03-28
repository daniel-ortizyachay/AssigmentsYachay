# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY recommendation_model.pkl recommendation_model.pkl
COPY user_factors.pkl user_factors.pkl
COPY movie_factors.pkl movie_factors.pkl

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8082
EXPOSE 8082

# Comando para ejecutar el servicio
CMD ["python", "app.py"]
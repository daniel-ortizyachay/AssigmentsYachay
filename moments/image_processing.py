import requests
import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def generate_alt_text(image_path):
    subscription_key = '9ZwEn34Zb5O1ET52W1w2D9HmILDf16Vt7yTtePT4s6SPBDCXbClfJQQJ99BCACYeBjFXJ3w3AAAFACOGLz1N'
    endpoint = 'https://visionlabsychay.cognitiveservices.azure.com/'
    analyze_url = endpoint + "vision/v3.1/analyze"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Description'}

    # Subir la imagen a Azure Blob Storage y obtener la URL pública
    public_image_url = upload_image_to_blob(image_path, "your-container-name", "your-blob-name")

    data = {'url': public_image_url}

    # Agregar una línea de registro para imprimir el valor de public_image_url
    logging.info(f"Sending request to Azure Vision API for image URL: {public_image_url}")

    response = requests.post(analyze_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    analysis = response.json()
    alt_text = analysis["description"]["captions"][0]["text"]
    return alt_text

def upload_image_to_blob(image_path, container_name, blob_name):
    connect_str = "DefaultEndpointsProtocol=https;AccountName=almacenamientophotos;AccountKey=JqjCt1IHMvJiOmOkaRE6JSXYUE7F2G9ufvNEKdsyVEpI4RfCxmwJLffUbRhb4n8pC5t4PXVFGjBU+ASt6nKp7A==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(image_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    return blob_client.url
import csv
from confluent_kafka import Consumer

def consume_kafka_stream(topic, bootstrap_servers, group_id, output_file):
    """Consumir mensajes de Kafka y guardarlos en un archivo CSV."""
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic])

    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "user_id", "server", "status", "result", "response_time"])  # Encabezados

            while True:
                msg = consumer.poll(1.0)  # Espera 1 segundo por mensajes
                if msg is None:
                    continue
                if msg.error():
                    print(f"Error: {msg.error()}")
                    continue

                # Procesar el mensaje
                message = msg.value().decode('utf-8')
                print(f"Received message: {message}")

                # Dividir el mensaje en columnas
                parts = message.split(",")
                if len(parts) >= 6:
                    writer.writerow(parts[:6])  # Guardar las primeras 6 columnas
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

# Configuración
consume_kafka_stream(
    topic="movielog1",
    bootstrap_servers="localhost:9092",
    group_id="data_collector_group",
    output_file="kafka_logs.csv"
)
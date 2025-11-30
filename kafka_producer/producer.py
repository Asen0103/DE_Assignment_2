from kafka import KafkaProducer
import csv
import json
import time

def kafka_python_producer_sync(producer, msg: str, topic: str):
    producer.send(topic, bytes(msg, encoding="utf-8"))
    print("Sending:", msg)
    producer.flush(timeout=60)


def success(metadata):
    print(metadata.topic, metadata.partiotion)


def error(exception):
    print(exception)


def kafka_python_producer_async(producer, msg: str, topic: str):
    """Send one message asynchronously (with callbacks)."""
    producer.send(topic, bytes(msg, encoding="utf-8")) \
            .add_callback(success) \
            .add_errback(error)
    producer.flush()


if __name__ == "__main__":
    # 1) Point this to YOUR VM’s external IP
    BOOTSTRAP_SERVERS = "35.202.186.2:9092"

    # 2) Path to the used-cars CSV on YOUR LAPTOP
    CSV_PATH = r""C:\Users\User\Downloads\vehicles.csv\vehicles.csv""

    TOPIC = "used_cars_stream"

    # Create the producer 
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

    # Open the CSV and stream it line by line
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Pick the fields you care about for streaming
            event = {
                "id": row.get("id"),
                "manufacturer": row.get("manufacturer"),
                "model": row.get("model"),
                "year": row.get("year"),
                "state": row.get("state"),
                "region": row.get("region"),
                "price": row.get("price"),
                "odometer": row.get("odometer"),
                "posting_date": row.get("posting_date"),
            }

            msg = json.dumps(event)

            # Send synchronously 
            kafka_python_producer_sync(producer, msg, TOPIC)

            # Small pause so it looks like a real-time stream
            time.sleep(0.2)

    print("Finished sending all events.")

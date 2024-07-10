import signal
import sys
from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'user-login',
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def process_data(data):
    # Here, we extract the user_id and convert the timestamp to a readable format.
    try:
        user_id = data.get('user_id')
        timestamp = data.get('timestamp')
        # Convert timestamp to human-readable format
        readable_timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

        # Create a new dictionary with transformed data
        processed_data = {
            'user_id': user_id,
            'app_version': data.get('app_version'),
            'device_type': data.get('device_type'),
            'ip': data.get('ip'),
            'locale': data.get('locale'),
            'device_id': data.get('device_id'),
            'timestamp': readable_timestamp
        }

        # Insight: log users using a specific app version
        if processed_data['app_version'] == '2.3.0':
            logger.info(f"User {user_id} is using app version 2.3.0")

        return processed_data
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return None

def main():
    logger.info("Starting Kafka consumer")
    try:
        for message in consumer:
            data = message.value
            logger.info(f"Received data: {data}")
            processed_data = process_data(data)
            if processed_data:
                producer.send('processed-topic', value=processed_data)
                logger.info(f"Processed data sent to 'processed-topic': {processed_data}")
    except Exception as e:
        logger.error(f"Error in Kafka consumer: {e}")

def signal_handler(sig, frame):
    logger.info("Gracefully shutting down...")
    consumer.close()
    producer.close()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()

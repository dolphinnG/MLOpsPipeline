from confluent_kafka import Producer, Consumer, KafkaError

# Kafka Producer
def produce_message(broker, topic, message, sasl_username, sasl_password):
    conf = {
        'bootstrap.servers': broker,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': sasl_username,
        'sasl.password': sasl_password
    }
    producer = Producer(**conf)

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.flush()



if __name__ == "__main__":
    broker = 'localhost:9092'
    topic = 'test_topic'
    group = 'test_group'
    message = 'Hello, Kafka!'
    sasl_username = 'user1'
    sasl_password = 'lC1hxSGxLk'

    produce_message(broker, topic, message, sasl_username, sasl_password)

# # Kafka Consumer
# from confluent_kafka import Producer, Consumer, KafkaError

# def consume_messages(broker, group, topic, sasl_username, sasl_password):
#     conf = {
#         'bootstrap.servers': broker,
#         'group.id': group,
#         'auto.offset.reset': 'earliest',
#         'security.protocol': 'SASL_SSL',
#         'sasl.mechanisms': 'SCRAM-SHA-256',
#         'sasl.username': sasl_username,
#         'sasl.password': sasl_password
#     }
#     consumer = Consumer(**conf)
#     consumer.subscribe([topic])

#     while True:
#         msg = consumer.poll(1.0)
#         if msg is None:
#             continue
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 continue
#             else:
#                 print(msg.error())
#                 break
#         print(f"Received message: {msg.value().decode('utf-8')}")

#     consumer.close()

# # Example usage
# if __name__ == "__main__":
#     broker = 'localhost:9092'
#     topic = 'test_topic'
#     group = 'test_group'
#     message = 'Hello, Kafka!'
#     sasl_username = 'user1'
#     sasl_password = 'lC1hxSGxLk'

#     consume_messages(broker, group, topic, sasl_username, sasl_password)
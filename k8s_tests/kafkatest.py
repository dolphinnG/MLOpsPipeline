from confluent_kafka.admin import AdminClient

# Configuration for the Kafka client
conf = {
    'bootstrap.servers': 'kafka-dolphin-service:9092',
    'sasl.mechanism': 'SCRAM-SHA-256',
    # 'security.protocol': 'SASL_PLAINTEXT',
    'security.protocol': 'SASL_SSL', # can use local trusted root CA when k8s bridge is established
    'sasl.username': 'user3',
    'sasl.password': 'password3',
    # 'ssl.ca.location': 'C:\\Users\\justm\\Desktop\\Pipeline\\helm\\files\\rootCA\\dolphin.rootCA.crt'
}

# Create an AdminClient instance
admin_client = AdminClient(conf)

# Query broker information
def list_brokers():
    cluster_metadata = admin_client.list_topics(timeout=10)
    brokers = cluster_metadata.brokers
    for broker_id, broker in brokers.items():
        print(f"Broker ID: {broker_id}, Broker Address: {broker.host}:{broker.port}")

if __name__ == "__main__":
    list_brokers()
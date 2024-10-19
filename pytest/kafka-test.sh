cat <<EOF > /tmp/client.properties
sasl.mechanism=SCRAM-SHA-256
security.protocol=SASL_SSL
ssl.truststore.location=/test/ssl/truststore.jks
ssl.truststore.password=lmaohehe
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
  username="user1" \
  password="password1";
EOF


kubectl run kafka-client -n dolphin-ns --rm -it --image=confluentinc/cp-kafka -- bash 


kafka-console-producer.sh --broker-list kafka-dolphin-service:9092 --topic test_topic --producer.config /tmp/client.properties

kafka-console-consumer.sh --bootstrap-server kafka-dolphin-service:9092 --topic dolphin-topic --from-beginning --consumer.config /tmp/client.properties

kafka-topics.sh --create --topic dolphin-topic --bootstrap-server kafka-dolphin-service:9092 --partitions 1 --replication-factor 1 --command-config /tmp/client.properties

kafka-console-producer.sh --broker-list kafka-dolphin-service:9092 --topic dolphin-topic --producer.config /tmp/client.properties


# Create the client.properties file
@"
sasl.mechanism=SCRAM-SHA-256
security.protocol=SASL_SSL
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
  username=\"user1\" \
  password=\"password1\";
"@ | Out-File -FilePath ".\testclient.properties" -Encoding ASCII



kubectl run kafka-dolphin-service-client --restart='Never' --image docker.io/bitnami/kafka:3.8.0-debian-12-r5 --namespace dolphin-ns --command -- sleep infinity
kubectl cp --namespace dolphin-ns .\testclient.properties kafka-dolphin-service-client:/tmp/client.properties
kubectl exec --tty -i kafka-dolphin-service-client --namespace dolphin-ns -- bash
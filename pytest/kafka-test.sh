cat <<EOF > /tmp/client.properties
sasl.mechanism=SCRAM-SHA-256
security.protocol=SASL_PLAINTEXT
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
  username="user1" \
  password="Ejq6hiYH6U";
EOF

kubectl run kafka-client -n dolphin-ns --rm -it --image=confluentinc/cp-kafka -- bash 


kafka-console-producer --broker-list kafkatest-controller-headless:9092 --topic test_topic --producer.config /tmp/client.properties

kafka-console-consumer --bootstrap-server kafkatest:9092 --topic test_topic --from-beginning --consumer.config /tmp/client.properties

kafka-topics --create --topic hahaha --partitions 1 --replication-factor 1 --bootstrap-server kafkatest:9092

kafka-console-producer --broker-list kafkatest:9092 --topic test_topic --producer.config /tmp/client.properties

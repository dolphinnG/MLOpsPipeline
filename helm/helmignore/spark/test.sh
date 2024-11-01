# ./bin/spark-submit \
#     --class org.apache.spark.examples.SparkPi \
#     --master k8s://https://kubernetes.default.svc.cluster.local:443 \
#     --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://sparktest-master-svc:7077 \
#     --conf spark.kubernetes.container.image=docker.io/bitnami/spark:3.5.3-debian-12-r0 \
#     --conf spark.kubernetes.file.upload.path=/tmp \
#     --conf spark.kubernetes.authenticate.caCertFile=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
#     --conf spark.kubernetes.authenticate.driver.caCertFile=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
#     --conf spark.kubernetes.authenticate.driver.mounted.caCertFile=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
#     --conf spark.kubernetes.namespace=dolphin-ns \
#     --conf spark.kubernetes.authenticate.driver.serviceAccountName=sparktest \
#     --deploy-mode cluster \
#     ./examples/jars/spark-examples_2.12-3.5.3.jar 1000

# ./bin/spark-submit \
#     --class org.apache.spark.examples.SparkPi \
#     --conf spark.kubernetes.container.image=bitnami/spark:latest \
#     --master k8s://https://kubernetes.default.svc.cluster.local:443 \
#     --conf spark.kubernetes.driverEnv.SPARK_MASTER_URL=spark://sparktest-master-svc:7077 \
#     --conf spark.kubernetes.file.upload.path=/tmp \
#     --conf spark.kubernetes.authenticate.clientCertFile=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
#     --conf spark.kubernetes.namespace=dolphin-ns \
#     --deploy-mode client \
#     ./examples/jars/spark-examples_2.12-3.5.3.jar 1000

./bin/spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --master spark://sparktest-master-svc:7077 \
    --deploy-mode client \
    ./examples/jars/spark-examples_2.12-3.5.3.jar 10
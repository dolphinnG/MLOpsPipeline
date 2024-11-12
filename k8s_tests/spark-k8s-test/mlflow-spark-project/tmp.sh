
spark-submit --master spark://sparktest-master-svc:7077 --total-executor-cores 1 --executor-memory 472M testspark2.py

mlflow run . --experiment-name spark-k8s-test --env-manager conda
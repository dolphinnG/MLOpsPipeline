import logging
import os
import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from mlflow.models import infer_signature
from pyspark.sql.functions import col
from pyspark.ml.functions import array_to_vector
import mlflow.pyfunc
import pandas as pd

logger = logging.getLogger(__name__)

# os.environ['MLFLOW_TRACKING_SERVER_CERT_PATH'] = "/etc/ssl/certs/ca-certificates.crt"
# os.environ['MLFLOW_TRACKING_USERNAME'] = "mlflow"
# os.environ['MLFLOW_TRACKING_PASSWORD'] = "mlflow"

def main():
    # os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://mlflowtest-minio:80"
    # os.environ['AWS_ACCESS_KEY_ID'] = "admin"
    # os.environ['AWS_SECRET_ACCESS_KEY'] = "admin123"
    # mlflow.set_tracking_uri("http://mlflowtest-tracking:80")
    
    # spark-submit --master spark://spark-master-svc:7077 testspark5.py
    mlflow.set_experiment("SPARK-TEST-5")
    
    logger.log(logging.INFO, "Starting the spark session")

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("gggg wwwww") \
        .config("spark.driver.host", os.environ.get("POD_IP")) \
        .getOrCreate()

    # Create a pandas DataFrame
    pandas_df = pd.DataFrame({
        "features": [[3.0, 4.0], [5.0, 6.0]],
        "label": [0, 1]
    })

    # Convert pandas DataFrame to Spark DataFrame
    train_df = spark.createDataFrame(pandas_df).select(array_to_vector("features").alias("features"), col("label"))

    lor = LogisticRegression(maxIter=2)
    lor.setPredictionCol("").setProbabilityCol("prediction")
    lor_model = lor.fit(train_df)

    test_df = train_df.select("features")
    prediction_df = lor_model.transform(train_df)
    prediction_df.printSchema() # prediction result is a vector of probabilities of the label classes summing up to 1
    
    res = prediction_df.select("prediction")
    signature = infer_signature(test_df, prediction_df)

    with mlflow.start_run() as run:
        model_info = mlflow.spark.log_model(
            lor_model,
            "model",
            # signature=signature,
            dfs_tmpdir="/opt/bitnami/spark/tmp/"
        )

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()
    

import logging
import os
import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline, Transformer
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col
import mlflow.pyfunc
from mlflow.models import infer_signature
import pandas as pd

logger = logging.getLogger(__name__)

class SelectPredictionTransformer(Transformer):
    def _transform(self, df):
        return df.select("prediction")

def main():
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://mlflowtest-minio:80"
    os.environ['AWS_ACCESS_KEY_ID'] = "admin"
    os.environ['AWS_SECRET_ACCESS_KEY'] = "admin123"
    mlflow.set_tracking_uri("http://mlflowtest-tracking:80")
    
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
    train_df = spark.createDataFrame(pandas_df)

    # Convert features column to VectorUDT
    vector_assembler = VectorAssembler(inputCols=["features"], outputCol="features_vec")
    train_df = vector_assembler.transform(train_df).select("features_vec", "label")

    lor = LogisticRegression(maxIter=2, featuresCol="features_vec", labelCol="label")
    lor.setPredictionCol("prediction")

    # Create a pipeline with the logistic regression model and the custom transformer
    pipeline = Pipeline(stages=[lor, SelectPredictionTransformer()])

    # Fit the pipeline model
    pipeline_model = pipeline.fit(train_df)

    # signature = infer_signature(train_df, pipeline_model.transform(train_df))
    
    with mlflow.start_run() as run:
        model_info = mlflow.spark.log_model(
            pipeline_model,
            "model",
            dfs_tmpdir="/opt/bitnami/spark/tmp/"
        )

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()
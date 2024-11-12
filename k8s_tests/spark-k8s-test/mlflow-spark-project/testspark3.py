import logging
import os
import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from mlflow.models.signature import ModelSignature, infer_signature
from mlflow.types.schema import Schema, ColSpec
from pyspark.sql.types import DoubleType, LongType, StructType, StructField
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.functions import vector_to_array

import mlflow.pyfunc
import pandas as pd

logger = logging.getLogger(__name__)

def main():
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://mlflowtest-minio:80"
    os.environ['AWS_ACCESS_KEY_ID'] = "admin"
    os.environ['AWS_SECRET_ACCESS_KEY'] = "admin123"
    mlflow.set_tracking_uri("http://mlflowtest-tracking:80")
    
    mlflow.set_experiment("SPARK-TEST-datatype")
    
    logger.log(logging.INFO, "Starting the spark session")

    spark = SparkSession.builder \
        .appName("Singular DataType Model") \
        .config("spark.driver.host", os.environ.get("POD_IP")) \
        .getOrCreate()

    # Create the training DataFrame with singular data types
    schema = StructType([
        StructField("feature1", DoubleType(), True),
        StructField("feature2", DoubleType(), True),
        StructField("label", LongType(), True)
    ])

    train_data = [
        (3.0, 4.0, 0),
        (5.0, 6.0, 1)
    ]

    train_df = spark.createDataFrame(train_data, schema=schema)

    # Combine feature columns into a single vector column
    assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")

    # Train the Logistic Regression model
    lor = LogisticRegression(featuresCol="features", labelCol="label", maxIter=2)

    # Create a pipeline with the assembler and logistic regression stages
    pipeline = Pipeline(stages=[assembler, lor])

    # Fit the pipeline to the training data
    pipeline_model = pipeline.fit(train_df)

    # Create the test DataFrame
    test_df = train_df.select("feature1", "feature2")

    # Transform the test DataFrame to get predictions
    prediction_df = pipeline_model.transform(test_df).select("features", "prediction")

    # Convert the features column from Vector to Array
    prediction_df = prediction_df.withColumn("features_array", vector_to_array(col("features")))

    # Split the features array back into feature1 and feature2 for the output schema
    prediction_df = prediction_df.withColumn("feature1", col("features_array").getItem(0))
    prediction_df = prediction_df.withColumn("feature2", col("features_array").getItem(1))

    # Manually create the model signature
    # input_schema = Schema([
    #     ColSpec("double", "feature1"),
    #     ColSpec("double", "feature2")
    # ])
    # output_schema = Schema([
    #     ColSpec("double", "feature1"),
    #     ColSpec("double", "feature2"),
    #     ColSpec("double", "prediction")
    # ])
    # signature = ModelSignature(inputs=input_schema, outputs=output_schema)
    signature = infer_signature(train_df, prediction_df)
    # Log the entire pipeline model with MLflow
    with mlflow.start_run() as run:
        model_info = mlflow.spark.log_model(
            pipeline_model,
            "model",
            signature=signature,
            dfs_tmpdir="/opt/bitnami/spark/tmp/"
        )

    spark.stop()
    
    # curl http://127.0.0.1:9898/invocations -H 'Content-Type: application/json' -d '{
    #     "inputs": {"feature1": 11.1, "feature2": 12.2}
    # }'

if __name__ == "__main__":
    main()
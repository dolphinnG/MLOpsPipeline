import os
import mlflow
import mlflow.spark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from mlflow.models import infer_signature, set_signature

# from dummy_class import A

os.environ['MLFLOW_TRACKING_USERNAME'] = "admin"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "password"
# os.environ['MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING'] = "true"
def main():
    # A()
    # spark-submit --master spark://spark-master:7077 testsparksubmit.py
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("gggg wwwww") \
        .getOrCreate()
        # .master("spark://spark-master:7077") \
            
            
        # .config("spark.hadoop.fs.s3a.access.key", "minio_user") \
        # .config("spark.hadoop.fs.s3.secret.key", "minio_password") \

    # spark.sparkContext.setLogLevel("DEBUG")
###############################################################################################
########## this credential part is only necessary if querying minio directly from spark
########## if you are using mlflow to log the model, you don't need this part,
########## because the minio interaction is proxied through mlflow
########## but you still need to set the environment variables for mlflow client to interact with minio (unrelated to spark btw)
    # MinIO configuration
    minio_endpoint = "http://minio:9000"
    minio_access_key = "minio_user"
    minio_secret_key = "minio_password"
    minio_bucket = "bucket"
    minio_path = "input.txt"
    # Set Hadoop configurations for MinIO
    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.endpoint", minio_endpoint)
    hadoop_conf.set("fs.s3a.access.key", minio_access_key)
    hadoop_conf.set("fs.s3a.secret.key", minio_secret_key)
    hadoop_conf.set("fs.s3a.path.style.access", "true")
    hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

    # Read CSV file from MinIO
    csv_file_path = f"s3a://{minio_bucket}/{minio_path}"
    # df = spark.read.csv(csv_file_path, header=True, inferSchema=True) # uncomment to read from minio
    # df.show()
###############################################################################################
    # Create or load a DataFrame
    data = [("Alice", 34, 1), ("Bob", 45, 0), ("Cathy", 29, 1), ("David", 40, 0)]
    columns = ["Name", "Age", "Label"]
    df = spark.createDataFrame(data, columns)

    # Assemble features
    assembler = VectorAssembler(inputCols=["Age"], outputCol="features")
    df = assembler.transform(df)

    # Split the data
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    # Train a logistic regression model using MLlib
    lr = LogisticRegression(featuresCol="features", labelCol="Label", maxIter=2)
    lr_model = lr.fit(train_df)

    # Make predictions
    predictions = lr_model.transform(test_df)

    # Evaluate the model
    evaluator = MulticlassClassificationEvaluator(labelCol="Label", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print(f"Accuracy: {accuracy}")
    
    signature = infer_signature(test_df, predictions)
    print(predictions)
    # set_signature(model_info.model_uri, signature)    
    
    # Collect model parameters and metrics to the driver
    model_params = lr_model.extractParamMap()
      
    # os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://minio:9000"
    # os.environ['AWS_ACCESS_KEY_ID'] = "minio_user"
    # os.environ['AWS_SECRET_ACCESS_KEY'] = "minio_password"
    # mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("lmaoexperiment")
    with mlflow.start_run():
        mlflow.log_param("model_type", "LogisticRegddression")
        for param, value in model_params.items():
            mlflow.log_param(param.name, value)
        mlflow.log_metric("accuracy", accuracy)
        
        # Load the model back and log it to MLflow
        # lr_model = mlflow.spark.load_model(lr_model)
        # os.environ["DISABLE_MLFLOWDBFS"] = "true"
        model_info = mlflow.spark.log_model(lr_model, "kekekemodel", signature=signature, dfs_tmpdir="/opt/bitnami/spark/tmp/")
        
        # m = mlflow.spark.load_model(model_info.model_uri)
        # # Example data similar to test_df
        # from pyspark.ml.linalg import Vectors
        # data = [("Bob", 45, 0, Vectors.dense([45.0]))]
        # columns = ["Name", "Age", "Label", "features"]

        # # Create a Spark DataFrame
        # spark_df = spark.createDataFrame(data, columns)

        # # Make predictions
        # predictions = m.transform(spark_df)
        # predictions.show()
        
        
        # # Example data similar to test_df
        # data = {
        #     "Name": ["Bob"],
        #     "Age": [45],
        #     "Label": [0],
        #     "features": [[45.0]]
        # }

        # # Create a pandas DataFrame
        # pandas_df = pd.DataFrame(data)
        # r = m.predict(pandas_df)
        # print(r)


    # Stop the Spark session
    spark.stop()
    
    


if __name__ == "__main__":
    main()
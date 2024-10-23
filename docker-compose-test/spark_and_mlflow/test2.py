# import os
# import mlflow
# import mlflow.spark
# from mlflow.models import infer_signature
# from pyspark.sql import SparkSession
# from pyspark.ml.feature import VectorAssembler
# from pyspark.ml.classification import LogisticRegression
# from pyspark.ml.evaluation import MulticlassClassificationEvaluator
# from pyspark.ml.functions import array_to_vector
# import pandas as pd
# from pyspark.sql.functions import col


# # Set environment variables for PySpark
# # os.environ['PYSPARK_PYTHON'] = './environment/bin/python'
# # os.environ['PYSPARK_DRIVER_PYTHON'] = '/mnt/c/Users/justm/Desktop/pytest/mlflow/myenv/bin/python'



# # Create Spark session
# spark = SparkSession.builder \
#     .appName("MLflow Spark Example") \
#     .master("spark://127.0.0.1:7077") \
#     .getOrCreate()

# train_df = spark.createDataFrame(
#     [([3.0, 4.0], 0), ([5.0, 6.0], 1)], schema="features array<double>, label long"
# ).select(array_to_vector("features").alias("features"), col("label"))
# lor = LogisticRegression(maxIter=2)
# lor.setPredictionCol("predictionset").setProbabilityCol("prediction")
# lor_model = lor.fit(train_df)

# test_df = train_df.select("features")
# prediction_df = lor_model.transform(train_df).select("prediction")

# signature = infer_signature(test_df, prediction_df)

# # Initialize MLflow experiment
# mlflow.set_tracking_uri("http://127.0.0.1:5000")
# mlflow.set_experiment("bbbbbbbbbbbbb")
# import os
# os.environ["DISABLE_MLFLOWDBFS"] = "True"
# with mlflow.start_run() as run:
#     model_info = mlflow.spark.log_model(
#         lor_model,
#         "model",
#         signature=signature,
#     )

# # The following signature is outputed:
# # inputs:
# #   ['features': SparkML vector (required)]
# # outputs:
# #   ['prediction': SparkML vector (required)]
# print(model_info.signature)

# loaded = mlflow.pyfunc.load_model(model_info.model_uri)

# test_dataset = pd.DataFrame({"features": [[1.0, 2.0]]})

# # `loaded.predict` accepts `Array[double]` type input column,
# # and generates `Array[double]` type output column.
# print(loaded.predict(test_dataset))

# # Stop Spark session
# spark.stop()
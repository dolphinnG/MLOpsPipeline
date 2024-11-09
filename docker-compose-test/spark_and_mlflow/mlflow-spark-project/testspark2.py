import logging
import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from mlflow.models import infer_signature
from pyspark.sql.functions import col
from pyspark.ml.functions import array_to_vector
import mlflow.pyfunc
import pandas as pd
import mlflow

# from dummy_class import A

def main():
    # A()
    # spark-submit --master spark://spark-master:7077 --num-executors 2 testsparksubmit.py
    
    # logging.getLogger("mlflow").setLevel(logging.DEBUG)

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("gggg wwwww") \
        .getOrCreate()
        # .master("spark://spark-master:7077") \
    # spark.sparkContext.setLogLevel("DEBUG")
            
            
        # .config("spark.hadoop.fs.s3a.access.key", "minio_user") \
        # .config("spark.hadoop.fs.s3.secret.key", "minio_password") \

    train_df = spark.createDataFrame(
        [([3.0, 4.0], 0), ([5.0, 6.0], 1)], schema="features array<double>, label long"
    ).select(array_to_vector("features").alias("features"), col("label"))
    lor = LogisticRegression(maxIter=2)
    lor.setPredictionCol("").setProbabilityCol("prediction")
    lor_model = lor.fit(train_df)

    test_df = train_df.select("features")
    prediction_df = lor_model.transform(train_df).select("prediction")

    signature = infer_signature(test_df, prediction_df)

    with mlflow.start_run() as run:
        model_info = mlflow.spark.log_model(
            lor_model,
            "model",
            signature=signature,
            dfs_tmpdir="/opt/bitnami/spark/tmp/"  
            # WE NEED TO SET THIS TO A DIRECTORY THAT IS WRITABLE BY THE SPARK USER
        )

    # The following signature is outputed:
    # inputs:
    #   ['features': SparkML vector (required)]
    # outputs:
    #   ['prediction': SparkML vector (required)]
    
    # print(model_info.signature)



    # LOADING IMMEADIATELY AFTER SAVING THE MODEL SOMETIMES CAUSES AN SPARK ERROR, DONT KNOW WHY
    # BUT THE MODEL IS STILL PROPERLY LOGGED TO MLFLOW AND CAN BE LOADED LATER
    
    # loaded = mlflow.pyfunc.load_model(model_info.model_uri )
    # test_dataset = pd.DataFrame({"features": [[1.0, 2.0]]})
    # # `loaded.predict` accepts `Array[double]` type input column,
    # # and generates `Array[double]` type output column.
    # print(loaded.predict(test_dataset))
    
    
    
    # curl http://127.0.0.1:9898/invocations -H 'Content-Type: application/json' -d '{
    #     "inputs": {"features": [11.1, 12.2]}
    # }'


    # Stop the Spark session
    spark.stop()
    
    


if __name__ == "__main__":
    main()
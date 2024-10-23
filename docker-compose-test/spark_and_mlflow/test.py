# import os
# from pyspark.sql import SparkSession

# os.environ['PYSPARK_PYTHON'] = '/mnt/c/Users/justm/Desktop/pytest/mlflow/myenv/bin/python'
# os.environ['PYSPARK_DRIVER_PYTHON'] = '/mnt/c/Users/justm/Desktop/pytest/mlflow/myenv/bin/python'
# # Initialize Spark session with necessary packages
# spark = SparkSession.builder \
#     .appName("SaveToMinIO") \
#     .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901") \
#     .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
#     .config("spark.hadoop.fs.s3a.path.style.access", "true") \
#     .getOrCreate()

# # Sample data
# data = [("John", 28), ("Anna", 23), ("Mike", 45)]
# columns = ["Name", "Age"]

# # Create DataFrame
# df = spark.createDataFrame(data, columns)

# # MinIO configuration
# minio_endpoint = "http://127.0.0.1:9000"
# minio_access_key = "minio_user"
# minio_secret_key = "minio_password"
# minio_bucket = "bucket"
# minio_path = "kakaka"

# # Set Hadoop configurations for MinIO
# hadoop_conf = spark._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.s3a.endpoint", minio_endpoint)
# hadoop_conf.set("fs.s3a.access.key", minio_access_key)
# hadoop_conf.set("fs.s3a.secret.key", minio_secret_key)
# hadoop_conf.set("fs.s3a.path.style.access", "true")
# hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# # Write DataFrame to MinIO
# df.write.csv(f"s3a://{minio_bucket}/{minio_path}")

# # Stop the Spark session
# spark.stop()
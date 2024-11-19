import os
import time
from SparkLauncher import SparkLauncher


spark_launcher = SparkLauncher()

log_file_name = spark_launcher.launch(
    properties_file="dolphin-spark.conf",
    python_entry_file="dummy_spark_project/testspark5.py",
    zip_file="./output.zip"
)

for line in spark_launcher.stream_logs(log_file_name):
    print(line, end='')
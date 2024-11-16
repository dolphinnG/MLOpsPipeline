import os
import time
from SparkService import SparkService

log_file_name = '/tmp/spark_job_aa043f59-0b5b-4a3e-ac77-3a072d0e9463.log'

spark_service = SparkService()

for line in spark_service.log_stream(log_file_name):
    print(line, end='')
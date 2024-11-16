import logging
import subprocess
import uuid
from SparkService import SparkLauncher

logging.basicConfig(level=logging.INFO)




if __name__ == "__main__":
    spark_service = SparkLauncher()
    properties_file = 'dolphin-spark.conf'
    file_name = 'testspark5.py'
    log_file_name = f"/tmp/spark_job_{uuid.uuid4()}.log"
    print(f"Log file generated: {log_file_name}")
    # probably spin a background thread to launch the spark job, 
    # while the main thread returns the log file name to user
    spark_service.submit_spark_job(properties_file, file_name, log_file_name)
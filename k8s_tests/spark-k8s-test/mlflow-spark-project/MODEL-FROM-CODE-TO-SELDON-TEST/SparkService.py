import logging
import subprocess
import time
import uuid


class SparkService:
    LOG_DONE = "dolphin_spark_done\n" 
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def submit_spark_job(self, properties_file, file_name, log_file_name):
        try:
            with open(log_file_name, 'a') as log_file:
                process = subprocess.Popen([
                    'spark-submit',
                    '--properties-file', properties_file,
                    file_name
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

                logging.info("Spark job submitted")
                # Stream the output to the log file
                for line in process.stdout:
                    log_file.write(line)
                    log_file.flush()
                
                process.wait()
                if process.returncode != 0:
                    log_file.write(f"An error occurred while submitting the Spark job: {process.returncode}\n")
                
                log_file.write(SparkService.LOG_DONE)

        except subprocess.CalledProcessError as e:
            with open(log_file_name, 'a') as log_file:
                log_file.write(f"An error occurred while submitting the Spark job: {e}\n")
                log_file.write(SparkService.LOG_DONE)
        
        # return log_file_name

    def log_stream(self, log_file_name):
        with open(log_file_name, 'r') as log_file:
            while True:
                line = log_file.readline()
                if line:
                    if line == SparkService.LOG_DONE:
                        break
                    yield line
                else:
                    time.sleep(1)  # Sleep briefly to avoid busy waiting
import logging
import subprocess
import time
import uuid
from BaseLauncher import BaseLauncher
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
class SparkLauncher(BaseLauncher):

    def launch(self, properties_file, python_entry_file, zip_file : str | None = None):
        log_file_path = self._generate_log_file_path("spark")
        try:
            command = ['spark-submit', '--properties-file', properties_file]
            if zip_file:
                command.extend(['--py-files', zip_file])
            command.append(python_entry_file)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            logger.info("Spark job submitted")
            log_thread = threading.Thread( #check if thread is fine
                target=self._accumulate_logs,
                args=(process, log_file_path),
            )
            log_thread.start()
        except subprocess.CalledProcessError as e:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"An error occurred while submitting the Spark job: {e}\n")
                log_file.write(BaseLauncher.LOG_DONE)
        finally:
            return log_file_path

    def _accumulate_logs(self, process, log_file_path):
        with open(log_file_path, 'a') as log_file:
            for line in process.stdout:
                log_file.write(line)
                log_file.flush()
            process.wait()
            if process.returncode != 0:
                log_file.write(f"An error occurred while submitting the Spark job: {process.returncode}\n")
            log_file.write(BaseLauncher.LOG_DONE)

    # log_stream method removed as it is now inherited from BaseService
import logging
import subprocess
import time
import threading
from BaseLauncher import BaseLauncher

class MLFlowService(BaseLauncher):
    LOG_DONE = "dolphin_mlflow_done\n"

    def __init__(self, project_uri, experiment_name):
        self.project_uri = project_uri
        self.experiment_name = experiment_name
        logging.basicConfig(level=logging.INFO)

    def launch(self, parameters=None):
        command = [
            "mlflow", "run",
            self.project_uri,
            "--experiment-name", self.experiment_name
        ]

        if parameters:
            for key, value in parameters.items():
                command.extend([f"--{key}", value])

        log_file_path = self._generate_log_file_path("mlflow")
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            logging.info("MLFlow job submitted")
            log_thread = threading.Thread( #check thread
                target=self._accumulate_logs,
                args=(process, log_file_path),
            )
            log_thread.start()
        except subprocess.CalledProcessError as e:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"An error occurred while running the MLFlow job: {e}\n")
                log_file.write(MLFlowService.LOG_DONE)
        finally:
            return log_file_path

    def _accumulate_logs(self, process, log_file_path):
        with open(log_file_path, 'a') as log_file:
            for line in process.stdout:
                log_file.write(line)
                log_file.flush()
            process.wait()
            if process.returncode != 0:
                log_file.write(f"An error occurred while running the MLFlow job: {process.returncode}\n")
            log_file.write(MLFlowService.LOG_DONE)
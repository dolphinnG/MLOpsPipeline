import logging
import subprocess
import time
import threading
from .BaseLauncher import BaseLauncher
from .S3Service import S3Service
from .ProjectModel import Project

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MLFlowLauncher(BaseLauncher):
    def __init__(self, s3_service: S3Service):
        super().__init__(s3_service=s3_service)

    def launch(self, project:Project):
        return self._launch(project.project_repo_url, project.project_parameters["experiment_name"])

    def _launch(self, project_uri, experiment_name):
        command = [
            "mlflow", "run",
            project_uri,
            "--experiment-name", experiment_name,
            "--storage-dir", "/tmp/mlprojects",
        ]

        # if parameters:
        #     for key, value in parameters.items():
        #         command.extend([f"--{key}", value])

        log_file_path = self._generate_log_file_path("mlflow")
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            logger.info("MLFlow job submitted")
            log_thread = threading.Thread( #check thread
                target=self._accumulate_logs,
                args=(process, log_file_path),
            )
            log_thread.start()
        except subprocess.CalledProcessError as e:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"An error occurred while running the MLFlow job: {e}\n")
                log_file.write(BaseLauncher.LOG_DONE)
        finally:
            return log_file_path

    def _accumulate_logs(self, process, log_file_path:str):
        with open(log_file_path, 'a') as log_file:
            for line in process.stdout:
                log_file.write(line)
                log_file.flush()
            process.wait()
            if process.returncode != 0:
                log_file.write(f"An error occurred while running the MLFlow job: {process.returncode}\n")
            log_file.write(BaseLauncher.LOG_DONE)
        # put log file to S3
        # log_file_path is "xxx.log"
        self.s3_service.put_log_file(log_file_path.split('/')[-1], log_file_path) 
        ...
import logging
import subprocess
import uuid
import zipfile
import git

from cv2 import log
from .BaseLauncher import BaseLauncher
import threading

import os
import shutil
from .ProjectModel import Project

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)



class SparkLauncher(BaseLauncher):

    def __init__(self, s3_service):
        super().__init__(s3_service)
        # TODO: .env this path
        self.properties_file = '/home/dolphin/Desktop/pipeline/MLOpsPipeline/microservices/deployment/launcher_tpm/project_router/dolphin-spark.conf'

    def _launch(self, python_entry_file, zip_file: str | None = None):
        log_file_path = self._generate_log_file_path("spark")
        try:
            command = ['spark-submit', '--properties-file', self.properties_file]
            if zip_file:
                command.extend(['--py-files', zip_file])
            command.append(python_entry_file)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            logger.info("Spark job submitted")
            log_thread = threading.Thread(
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

    # def _git_clone(self, repo_url, repo_dir):
    #     command = ['git', 'clone', repo_url, repo_dir]
    #     subprocess.run(command, check=True)
    
    def _git_clone(self, repo_url, repo_dir):
        git.Repo.clone_from(repo_url, repo_dir)
        # pip install gitpython , still needs git installed on the system
        
    def _zip_project(self, project_dir):
        zip_file = f"{project_dir}.zip"
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=project_dir)
                    zipf.write(file_path, arcname)
        return zip_file

    def launch(self, project:Project):
        repo_url = project.project_repo_url
        entry_module = project.project_entry_module
        tmp_git_dir = f"/tmp/spark-project-{uuid.uuid4()}"
        if os.path.exists(tmp_git_dir):
            shutil.rmtree(tmp_git_dir)
        os.makedirs(tmp_git_dir)

        # Clone the project
        self._git_clone(repo_url, tmp_git_dir)

        # Find the testspark5.py file
        entry_file_path = None
        for root, dirs, files in os.walk(tmp_git_dir):
            if entry_module in files:
                entry_file_path = os.path.join(root, entry_module)
                break

        if not entry_file_path:
            raise FileNotFoundError("testspark5.py not found in the cloned repository")

        # Zip the project
        zip_file_path = self._zip_project(tmp_git_dir)

        # Launch the project
        log_file_path = self._launch(entry_file_path, zip_file_path)
    
        # Remove the zip file and the cloned project directory
        # TODO: code to remove the tmp dir and tmp zip file without race condition
        # os.remove(zip_file_path)
        # shutil.rmtree(tmp_git_dir)
        
        return log_file_path
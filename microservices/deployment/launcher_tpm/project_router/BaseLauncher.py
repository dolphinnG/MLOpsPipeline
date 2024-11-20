from abc import ABC, abstractmethod
import time
import logging
import os
import tempfile
import uuid
from .S3Service import S3Service
from .ProjectModel import Project

class BaseLauncher(ABC):
    LOG_DONE = "dolphin_done"
    
    def __init__(self, s3_service: S3Service) -> None:
        self.s3_service = s3_service
    
    # @abstractmethod
    # def launch(self, *args, **kwargs) -> str:
    #     ...
    @abstractmethod
    def launch(self, project:Project) -> str:
        ...
        
    def stream_logs(self, log_file_path):
        with open(log_file_path, 'r') as log_file:
            while True:
                line = log_file.readline()
                if line:
                    if line.strip() == BaseLauncher.LOG_DONE:
                        break
                    # time.sleep(1) # TODO: REMEMBER TO REMOVE THIS!!!!
                    yield line
                else:
                    time.sleep(1)  # Sleep briefly to avoid busy waiting

    def _generate_log_file_path(self, prefix="log"):
        log_file_path = os.path.join(tempfile.gettempdir(), f"{prefix}_{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.log")
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"")
        return log_file_path
    
    @abstractmethod
    def _accumulate_logs(self, *args, **kwargs) -> str:
        ...
    
    def _save_logs(self, *args, **kwargs) -> None:
        log_file_path =  self._accumulate_logs(*args, **kwargs)
        self.s3_service.put_log_file(log_file_path.split('/')[-1], log_file_path)
        
from abc import ABC, abstractmethod
import time
import logging
import os
import tempfile
import uuid

class BaseLauncher(ABC):
    LOG_DONE = "dolphin_done"
    @abstractmethod
    def launch(self, *args, **kwargs) -> str:
        ...

    def stream_logs(self, log_file_path):
        with open(log_file_path, 'r') as log_file:
            while True:
                line = log_file.readline()
                if line:
                    if line.strip() == BaseLauncher.LOG_DONE:
                        break
                    yield line
                else:
                    time.sleep(1)  # Sleep briefly to avoid busy waiting

    def _generate_log_file_path(self, prefix="log"):
        return os.path.join(tempfile.gettempdir(), f"{prefix}_{uuid.uuid4()}.log")
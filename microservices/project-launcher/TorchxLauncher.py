import logging
from torchx import runner
from torchx.components.dist import ddp
import time
from torchx.runner.api import Stream
from kubernetes import client, config
from BaseService import ILauncher
import os
import tempfile
import threading


class TorchxLauncher(ILauncher):
    def __init__(self, namespace, queue):
        self.namespace = namespace
        self.queue = queue
        self.session = runner.get_runner()
        self.run_cfg = {"namespace": namespace, "queue": queue}
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        
    @classmethod
    def create_ddp_component(
        cls,
        job_name,
        module_name,
        env,
        j="1x2",
        image="supahakka/launcher:v21",
        cpu=1,
        rdzv_backend="c10d",
        rdzv_port=30303,
    ):
        return ddp(
            m=module_name,
            image=image,
            name=job_name,
            cpu=cpu,
            rdzv_backend=rdzv_backend,
            rdzv_port=rdzv_port,
            env=env,
            j=j,
        )

    def _accumulate_logs(self, app_handle, log_file_path, role_name):
        with open(log_file_path, "a") as log_file:
            for line in self.session.log_lines(
                app_handle=app_handle,
                role_name=role_name,
                k=0,
                streams=Stream.COMBINED,
                should_tail=True,
            ):
                log_file.write(line)
                # logging.info(line)

    def launch(self, ddp_component):
        log_file_path = self._generate_log_file_path(ddp_component.roles[0].name)
        try:
            app_handle = self.session.run(
                ddp_component, scheduler="kubernetes", cfg=self.run_cfg, workspace=""
            )
            logging.info(self.session.status(app_handle))
            logging.info("---" * 10)
            logging.info(f"== {ddp_component.roles[0].name} rank 0 logs ==")

            log_thread = threading.Thread( #check if thread is fine
                target=self._accumulate_logs,
                args=(app_handle, log_file_path, ddp_component.roles[0].name),
            )
            log_thread.start()
            # self.stream_logs(log_file_path)

        finally:
            # self.session.close()
            return log_file_path

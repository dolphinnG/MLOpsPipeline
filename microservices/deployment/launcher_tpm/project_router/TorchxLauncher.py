import logging
from torchx import runner
from torchx.components.dist import ddp
import time
from torchx.runner.api import Stream
from kubernetes import client, config

from .ProjectModel import Project
from .BaseLauncher import BaseLauncher
import threading


class TorchxLauncher(BaseLauncher):
    def __init__(self, namespace, queue, s3_service):
        self.namespace = namespace
        self.queue = queue
        self.session = runner.get_runner()
        self.run_cfg = {"namespace": self.namespace, "queue": self.queue}
        # config.load_incluster_config()
        # self.v1 = client.CoreV1Api()
        super().__init__(s3_service=s3_service)
        
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
        # logging.info(f"Accumulating lossgs for {role_name}")
        with open(log_file_path, "a") as log_file:
            while True:
                try:
                    # logging.info("streaming logs")
                    log_iter = self.session.log_lines(
                        app_handle=app_handle,
                        role_name=role_name,
                        k=0,
                        streams=Stream.COMBINED,
                        should_tail=True
                        )
                    for line in log_iter:
                        log_file.write(line+"\n") 
                    log_file.write(BaseLauncher.LOG_DONE)
                    break  
                except client.ApiException as e:
                    logging.error(f"Error streaming logs {e}:  -- retrying in 5s")
                    time.sleep(5)
        return log_file_path
       
                    

    def launch(self, project: Project) -> str:
        module_name = project.project_entry_module.split(".")[-2]
        job_name = project.project_parameters['job_name']
        ddp_component = TorchxLauncher.create_ddp_component(
            job_name=job_name, # add the html form
            module_name=module_name, # strip the .py
            # image="supahakka/launcher:v21",
            image=project.project_repo_url,
            # cpu=1,
            # rdzv_backend="c10d",
            # rdzv_port=30303,
            j="2x1",
            env={ # .env this shit
                "MLFLOW_S3_ENDPOINT_URL": "http://mlflowtest-minio:80",
                "MLFLOW_TRACKING_URI": "http://mlflowtest-tracking:80",
                "AWS_ACCESS_KEY_ID": "admin",
                "AWS_SECRET_ACCESS_KEY": "admin123",
                "MLFLOW_EXPERIMENT_NAME": "topg" # TODO: had better set in the script
            }
        )
        return self._launch(ddp_component)
    
    def _launch(self, ddp_component):
        log_file_path = self._generate_log_file_path(ddp_component.roles[0].name)
        # with open(log_file_path, "w") as log_file:
        #     log_file.write("")
        try:
            app_handle = self.session.run(
                ddp_component, scheduler="kubernetes", cfg=self.run_cfg, workspace=""
            )
            logging.info(self.session.status(app_handle))
            logging.info("---" * 10)
            logging.info(f"== {ddp_component.roles[0].name} rank 0 logs ==")

            log_thread = threading.Thread( #check if thread is fine
                target=self._save_logs,
                args=(app_handle, log_file_path, ddp_component.roles[0].name),
            )
            log_thread.start()
            # self.stream_logs(log_file_path)
        except Exception as e:
            logging.error(f"Error launching job: {e}")
        finally:
            # self.session.close()
            return log_file_path

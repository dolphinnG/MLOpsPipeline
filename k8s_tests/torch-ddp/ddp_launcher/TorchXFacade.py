import logging
from torchx import runner
from torchx.components.dist import ddp
import time
from torchx.runner.api import Stream
from kubernetes import client, config


class TorchXFacade:
    def __init__(self, namespace, queue):
        self.namespace = namespace
        self.queue = queue
        self.session = runner.get_runner()
        self.run_cfg = {"namespace": namespace, "queue": queue}
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()

    def create_ddp_component(
        self, job_name, module_name, env, j="1x2", image="supahakka/launcher:v21", cpu=1, rdzv_backend="c10d", rdzv_port=30303
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

    def stream_logs(self, app_handle, role_name):
        # role_name is module name. The constructed pod name must be correct for this to work
        def _stream_logs_inner(app_handle):
            for line in self.session.log_lines(
                app_handle=app_handle,
                role_name=role_name,
                k=0,
                streams=Stream.COMBINED,
                should_tail=True,
            ):
                logging.info(line)  
                # BUT IF YOU TAIL LOGS, YOU MUST ADD NEWLINE YOURSELF

        # def _is_pod_ready(pod_name, namespace):
        #     pod = self.v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        #     for container_status in pod.status.container_statuses:
        #         if (
        #             container_status.state.waiting
        #             and container_status.state.waiting.reason == "ContainerCreating"
        #         ):
        #             logging.info(f"Container {container_status.name} is still creating...")
        #             return False
        #     return True

        while True:
            try:
                # Check if the pod is ready
                # app_handle example: kubernetes://torchx/dolphin-ns:lmao-zgzw40cv9q00s
                # pod_name = app_handle.split("/")[-1]  
                # while not _is_pod_ready(pod_name, self.namespace):
                #     logging.info(f"Pod {pod_name} is still pulling the image...")
                #     time.sleep(10)

                _stream_logs_inner(app_handle)
                break  # Exit the loop when done
            except client.ApiException as e:
                # logging.error(f"Exception: {e}")
                logging.warning("pods not ready yet, retrying in 15 seconds...")
                time.sleep(15)

    def launch(self, ddp_component):
        try:
            app_handle = self.session.run(
                ddp_component, scheduler="kubernetes", cfg=self.run_cfg, workspace=""
            )
            logging.info(self.session.status(app_handle))

            # app_list = self.session.list("kubernetes")
            # logging.info("---" * 10)
            # for app in app_list:
            #     logging.info(f"app id: {app.app_id}, handle: {app.app_handle}, state: {app.state}")
            
            logging.info("---" * 10)
            logging.info(f"== {ddp_component.roles[0].name} rank 0 logs ==")
            self.stream_logs(app_handle, ddp_component.roles[0].name)
            
        finally:
            self.session.close()

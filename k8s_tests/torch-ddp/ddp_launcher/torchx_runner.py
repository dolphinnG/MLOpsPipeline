import logging
from torchx import runner
from torchx.components.dist import ddp
import time
from torchx.runner.api import Stream
import kubernetes
from TorchXFacade import TorchxLauncher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

namespace = "dolphin-ns"
queue = "default"
torchx_facade = TorchxLauncher(namespace, queue)

ddp_component = torchx_facade.create_ddp_component(
    job_name='lmao',
    module_name="ddptest",
    # image="supahakka/launcher:v21",
    # cpu=1,
    # rdzv_backend="c10d",
    # rdzv_port=30303,
    # j="2x2",
    env={
        "MLFLOW_S3_ENDPOINT_URL": "http://mlflowtest-minio:80",
        "MLFLOW_TRACKING_URI": "http://mlflowtest-tracking:80",
        "AWS_ACCESS_KEY_ID": "admin",
        "AWS_SECRET_ACCESS_KEY": "admin123",
        "MLFLOW_EXPERIMENT_NAME": "topg"
    }
)

try:
    torchx_facade.launch(ddp_component)
finally:
    torchx_facade.session.close()
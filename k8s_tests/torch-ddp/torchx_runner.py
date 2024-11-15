
from torchx import runner
from torchx.components.dist import ddp
import time
from torchx.runner.api import Stream
import kubernetes

session = runner.get_runner()
module_name = "ddptest"
ddp_component = ddp(
    m=module_name,
    image="supahakka/launcher:v21",
    name = 'lmao',
    cpu=1,
    rdzv_backend="c10d",
    rdzv_port=30303,
    env={
        "MLFLOW_S3_ENDPOINT_URL": "http://mlflowtest-minio:80",
        "MLFLOW_TRACKING_URI": "http://mlflowtest-tracking:80",
        "AWS_ACCESS_KEY_ID": "admin",
        "AWS_SECRET_ACCESS_KEY": "admin123",
        "MLFLOW_EXPERIMENT_NAME": "topg"
    },
    j="2x2"
)

run_cfg = {
    "namespace": "dolphin-ns",
    "queue": "default"
}
try:
    app_handle = session.run(ddp_component, scheduler="kubernetes", cfg=run_cfg, workspace="",)
    
    print(session.status(app_handle))
    
    app_list = session.list("kubernetes")
    print("---" * 10)
    for app in app_list:
        print(f"app id: {app.app_id}, handle: {app.app_handle}, state: {app.state}")
    # print("---" * 10)
    
    print("== trainer node 0 logs ==")
    while str(session.status(app_handle).state) != "PENDING":
        print("app PENDING")
        time.sleep(5)  # wait for 5 seconds before checking again

    # could cause exception if the pod has not been started, e.g image still pulling  
    def stream_logs(app_handle):
        for line in session.log_lines(app_handle=app_handle, role_name=module_name, k=0, streams=Stream.COMBINED, should_tail=True):
            # for prints newlines will already be present in the line
            print(line, end="\n") # BUT IF YOU TAIL LOGS, YOU MUST ADD NEWLINE YOURSELF
    done=False       
    while not done:
        try:
            stream_logs(app_handle)
            done=True
        except kubernetes.client.ApiException as e:
            print(f"Exception: {e}")
            time.sleep(5)
    



    
    # session.wait(app_handle)
    # time.sleep(5)
    # session.cancel(app_handle) # can only cancel running apps

finally:
    session.close()
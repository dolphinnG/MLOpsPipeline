# import datetime
# import pendulum

# from airflow.utils.state import DagRunState, TaskInstanceState
# from airflow.utils.types import DagRunType
# from airflow.models.dag import DAG
# from airflow.decorators import task


# DATA_INTERVAL_START = pendulum.datetime(2021, 9, 13, tz="UTC")
# DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)

# @task(task_id='hello_torchx')
# def run_torchx(message):
#     """This is a function that will run within the DAG execution"""
#     from torchx.runner import get_runner
#     import logging 
#     logger = logging.getLogger(__name__)
#     logger.info("Running TorchX job with message: %s", message)
#     with get_runner() as runner:
#         # Run the utils.sh component on the local_cwd scheduler.
#         app_id = runner.run_component(
#             "utils.echo",
#             ["--msg", "message"],
#             scheduler="local_cwd",
#         )

#         # Wait for the job to complete
#         status = runner.wait(app_id, wait_interval=1)
#         logger.info("Job completed with status: %s", status)
#         # Raise_for_status will raise an exception if the job didn't succeed
#         status.raise_for_status()

#         # Finally we can print all of the log lines from the TorchX job so it
#         # will show up in the workflow logs.
#         for line in runner.log_lines(app_id, "sh", k=0):
#             print(line, end="")

# with DAG(
#     dag_id='test-torchx',
#     schedule_interval=None,
#     catchup=False,
#     tags=['example'],
# ) as dag:
#     run_job = run_torchx("Hello, TorchX!")
    

# # torchx run -s kubernetes -cfg namespace=dolphin-ns,serviceaccount=airflow-sa,queue=dolphin-queu --workspace="" utils.echo --msg lmaohehehehe
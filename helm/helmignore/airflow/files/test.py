from torchx.runner import get_runner
import logging 
logger = logging.getLogger(__name__)
message = "Hello, TorchX!"
logger.info("Running TorchX job with message: %s", message)
with get_runner() as runner:
    # Run the utils.sh component on the local_cwd scheduler.
    app_id = runner.run_component(
        "utils.sh",
        ["echo", message],
        scheduler="local_cwd",
    )

    # Wait for the job to complete
    status = runner.wait(app_id, wait_interval=1)
    logger.info("Job completed with status: %s", status)
    # Raise_for_status will raise an exception if the job didn't succeed
    status.raise_for_status()

    # Finally we can print all of the log lines from the TorchX job so it
    # will show up in the workflow logs.
    for line in runner.log_lines(app_id, "sh", k=0):
        print(line, end="")
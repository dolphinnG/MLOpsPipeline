from pprint import pprint
from VolcanoFacade import VolcanoFacade
import json
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    facade = VolcanoFacade()
    jobs = facade.list_jobs()
    jobs_json = [job.model_dump() for job in jobs]
    logging.info(json.dumps(jobs_json, indent=4))
    for job in jobs:
        if job.succeeded or job.failed :
            facade.delete_job(job.name)
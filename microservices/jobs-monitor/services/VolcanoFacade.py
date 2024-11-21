import subprocess
from pydantic import BaseModel
from typing import List
import logging
from models.VolcanoModel import VolcanoJob

logging.basicConfig(
    format='%(asctime)s %(filename)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

class VolcanoFacade:
    def list_jobs(self, namespace='dolphin-ns') -> List[VolcanoJob]:
        try:
            result = subprocess.run(['vcctl', 'job', 'list', '-n', namespace], capture_output=True, text=True, check=True)
            output = result.stdout
            jobs = []
            for line in output.splitlines():
                if line.startswith('Name'):
                    continue
                parts = line.split()
                if len(parts) >= 10:  # Ensure there are enough parts in the line
                    job = VolcanoJob(
                        name=parts[0],
                        creation_date=parts[1],
                        phase=parts[2],
                        type=parts[3],
                        replicas=parts[4],
                        min_replicas=parts[5],
                        pending=int(parts[6]),
                        running=int(parts[7]),
                        succeeded=int(parts[8]),
                        failed=int(parts[9]),
                        unknown=int(parts[10]),
                        retry_count=parts[11]
                    )
                    jobs.append(job)
            return jobs
        except subprocess.CalledProcessError as e:
            logging.error(f"Error occurred while calling vcctl: {e}")
            return []

    def delete_job(self, job_name, namespace='dolphin-ns'):
        try:
            subprocess.run(['vcctl', 'job', 'delete', '-N', job_name, '-n', namespace], check=True)
            logging.info(f"Job {job_name} deleted successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error occurred while deleting job {job_name}: {e}")


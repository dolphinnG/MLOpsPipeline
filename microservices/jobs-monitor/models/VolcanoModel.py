
from pydantic import BaseModel


class VolcanoJob(BaseModel):
    name: str
    creation_date: str
    phase: str
    type: str
    replicas: str
    min_replicas: str
    pending: int
    running: int
    succeeded: int
    failed: int
    unknown: int
    retry_count: str
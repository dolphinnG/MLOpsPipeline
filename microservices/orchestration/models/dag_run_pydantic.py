
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class DAGRunPydantic(BaseModel):
    dag_run_id: str | None = Field(default_factory=lambda: 'run-' + datetime.now(timezone.utc).isoformat())
    execution_date: str|None = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    # state: str|None = "success"
    conf: dict | None = {}
    
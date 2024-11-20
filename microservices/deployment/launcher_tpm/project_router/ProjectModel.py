
from typing import Literal
from pydantic import BaseModel


class Project(BaseModel):
    project_name: str
    project_type: Literal["MLFLOW_SINGLE_NODE", "MLFLOW_TORCHDDP", "MLFLOW_SPARK"]
    # project_type: str
    creation_date: str
    project_repo_url: str
    project_entry_module: str
    project_parameters: dict[str, str] = {"experiment_name": ""}
from tempfile import tempdir
import tempfile
from cv2 import log
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, RedirectResponse
from datetime import datetime
import os
from pydantic import BaseModel, Field
from typing import List, Literal
from .deps import (
    get_launchers,
    get_s3_service,
    get_mlflow_launcher,
    get_torchx_launcher,
    get_spark_launcher,
)
from .BaseLauncher import BaseLauncher
from .MLFlowLauncher import (
    MLFlowLauncher,
)
from .SparkLauncher import SparkLauncher
from .ProjectModel import Project


launcherRouter = APIRouter()
dummy_project_data = [ # use redis persistence instead of sql
    {
        "project_name": "test-mlflow-project-run",
        "project_type": "MLFLOW_SINGLE_NODE",
        "creation_date": datetime(2021, 9, 1).strftime("%Y-%m-%d"),
        "project_repo_url": "https://github.com/dolphinnG/testmlproject.git",
        "project_entry_module": "main.py",
        "project_parameters": {"experiment_name": "test-mlflow-project-run"},
        "project_log_records": ["run-1", "run-2", "run-3", "dummy-log"],
    },
    {
        "project_name": "test-spark-project",
        # ADD RANDOMIZED UUID TO ENFORCE project_name UNIQUENESS OTHERWISE LOG VIEW UI MALFUNCTIONS
        "project_type": "MLFLOW_SPARK",
        "creation_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "project_repo_url": "https://github.com/dolphinnG/testsparkproject.git",
        "project_entry_module": "testspark5.py",
        "project_parameters": {},
        "project_log_records": [],
    },
    {
        "project_name": "testsfgyyysadfsdafsadfsdn",
        # ADD RANDOMIZED UUID TO ENFORCE project_name UNIQUENESS OTHERWISE LOG VIEW UI MALFUNCTIONS
        "project_type": "MLFLOW_TORCHDDP",
        "creation_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "project_repo_url": "sdfasdfasdf",
        "project_entry_module": "ddptest.py",
        "project_parameters": {},
        "project_log_records": [],
    },
    {
        "project_name": "test torch ddp launch",
        "project_type": "MLFLOW_TORCHDDP",
        "creation_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "project_repo_url": "supahakka/launcher:v21",
        "project_entry_module": "ddptest.py",
        "project_parameters": {"job_name": "hehejobsname"},
        "project_log_records": ["dummy-log"],
    },
]

templates = Jinja2Templates(directory="templates")



@launcherRouter.get("/projects")
async def get_projects(request: Request):
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": dummy_project_data}
    )


@launcherRouter.get("/projects/logs/{log_name}")
async def get_log_stream(log_name: str, launchers=Depends(get_launchers)):
    launcher: BaseLauncher = launchers.get("MLFLOW_SINGLE_NODE")  # any launcher will do

    log_file_name = f"{log_name}.log"
    log_file_path = os.path.join(tempfile.gettempdir(), log_file_name)

    if not os.path.exists(log_file_path):
        launcher.s3_service.get_log_file(log_file_name, log_file_path)

    log_stream = launcher.stream_logs(log_file_path)
    return StreamingResponse(log_stream, media_type="text/plain")


@launcherRouter.get("/create_project")
async def create_project_form(request: Request):
    return templates.TemplateResponse("create_project.html", {"request": request})


# pip install python-multipart
@launcherRouter.post("/create_project")
async def create_project(
    project_name: str = Form(...),
    project_type: str = Form(...),
    project_repo_url: str = Form(...),
    project_entry_module: str = Form(...),
    experiment_name: str = Form(None),
    job_name: str = Form(None)
):
    project_parameters = {}
    if project_type == "MLFLOW_SINGLE_NODE" and experiment_name:
        project_parameters["experiment_name"] = experiment_name
    elif project_type == "MLFLOW_TORCHDDP":
        project_parameters["job_name"] = job_name
    new_project = {
        "project_name": project_name,
        "project_type": project_type,
        "creation_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "project_repo_url": project_repo_url,
        "project_entry_module": project_entry_module,
        "project_parameters": project_parameters,
        "project_log_records": [],
    }
    dummy_project_data.append(new_project)
    return RedirectResponse(url="/launcher/projects", status_code=303)





os.environ["MLFLOW_TRACKING_URI"] = "http://127.0.0.1:5000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://127.0.0.1:9900"
os.environ["AWS_ACCESS_KEY_ID"] = "minio_user"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password"


# log_bucket_name = "projectlogs"


@launcherRouter.post("/launch")
async def launch_project(project: Project, launchers:dict[str, BaseLauncher]=Depends(get_launchers)):
    launcher = launchers.get(project.project_type)
    assert launcher is not None, f"Launcher for project type {project.project_type} not found!"
    # if project.project_type == "MLFLOW_SINGLE_NODE":
    #     log_file_path = launcher.launch(project=project)
    # elif project.project_type == "MLFLOW_SPARK":
    #     log_file_path = launcher.launch(project=project)
    log_file_path = launcher.launch(project=project)
    
    log_file_path = log_file_path.replace(".log", "")
    extracted_log_name = log_file_path.split("/")[-1]
    for proj in dummy_project_data:
        if proj["project_name"] == project.project_name:
            proj["project_log_records"].append(extracted_log_name)
            break
    return {"message": f"Project {project.project_name} launched successfully!"}
    # return {"message": "Project type not supported!"}

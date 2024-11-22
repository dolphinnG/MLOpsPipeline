import json
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import auth, user, mlflow, dag, dag_run, monitor, launch, Scheduler, Dataplane
from middlewares.TokenValidationMiddleware import TokenValidationMiddleware
from middlewares.ExceptionHandlingMiddleware import ExceptionHandlingMiddleware

from utils.constants import USER_SESSION_KEY, USER_DATA_KEY

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add custom filter to Jinja2 templates
templates.env.filters['load_json'] = json.loads

# Include router
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/users")
app.include_router(mlflow.router, prefix="/mlflow")
app.include_router(dag.router, prefix="/airflow")
app.include_router(dag_run.router, prefix="/airflow")
app.include_router(monitor.router, prefix="/distributed")
app.include_router(launch.router, prefix="/launcher")
app.include_router(Scheduler.router, prefix="/scheduler")
app.include_router(Dataplane.router, prefix="/dataplane")

# Add middleware
app.add_middleware(TokenValidationMiddleware)
app.add_middleware(ExceptionHandlingMiddleware)

@app.get("/")
async def read_root(request: Request):
    cookies = request.cookies
    return templates.TemplateResponse("index.html", {"request": request, "cookies": cookies})

@app.get("/protected")
async def protected(request: Request):
    user_session = request.cookies.get(USER_SESSION_KEY)
    return templates.TemplateResponse(
        "protected.html", {"request": request, "user_session": user_session}
    )

@app.get("/profile")
async def profile(request: Request):
    user_data = request.cookies.get(USER_DATA_KEY)
    assert user_data is not None, "User data not found in cookies"
    user_data_dict = json.loads(user_data)
    return templates.TemplateResponse("profile.html", {"request": request, "user_data_dict": user_data_dict})

# @app.get("/dag")
# async def dag(request: Request):
#     return templates.TemplateResponse("dag.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=14999, reload=True)

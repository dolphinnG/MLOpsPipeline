import json
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from routers import (
    auth,
    user,
    mlflow,
    dag,
    dag_run,
    monitor,
    launch,
    Scheduler,
    Dataplane,
)
from middlewares.TokenValidationMiddleware import TokenValidationMiddleware
from middlewares.ExceptionHandlingMiddleware import ExceptionHandlingMiddleware
from middlewares.PopulateRequestStateMiddleware import PopulateRequestStateMiddleware
from dependencies.deps import get_configurations
from utils.constants import USER_SESSION_KEY, USER_DATA_KEY

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()

# Add HTTPS redirect middleware
# app.add_middleware(HTTPSRedirectMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add custom filter to Jinja2 templates
templates.env.filters["load_json"] = json.loads

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
app.add_middleware(PopulateRequestStateMiddleware)
app.add_middleware(TokenValidationMiddleware)
app.add_middleware(ExceptionHandlingMiddleware) 

@app.get("/")
async def read_root(request: Request):
    cookies = request.cookies
    return templates.TemplateResponse(
        "index.html", {"request": request, "cookies": cookies}
    )

@app.get("/profile")
async def profile(request: Request):
    user_data = request.cookies.get(USER_DATA_KEY)
    assert user_data is not None, "User data not found in cookies"
    user_data_dict = json.loads(user_data)
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user_data_dict": user_data_dict}
    )

# Health check endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/liveness")
async def liveness_check():
    return {"status": "alive"}

@app.get("/readiness")
async def readiness_check():
    # Add any necessary checks to determine if the app is ready to serve traffic
    return {"status": "ready"}

settings = get_configurations()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=14999,
        # reload=True,
        ssl_certfile=settings.SERVER_CERT_PATH,
        ssl_keyfile=settings.SERVER_KEY_PATH,
    )  # TODO: set workers
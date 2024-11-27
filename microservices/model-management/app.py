import logging
from fastapi import FastAPI
from routers import mlflow
from dependencies.deps import get_settings
from utils.utils import set_env
from middlewares.ExceptionHandlingMiddleware import ExceptionHandlingMiddleware
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

set_env()
settings = get_settings()

app = FastAPI()


app.include_router(mlflow.router, prefix="/mlflow")

app.add_middleware(ExceptionHandlingMiddleware)
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=15000,
        # reload=True,
        ssl_certfile=settings.SERVER_CERT_PATH,
        ssl_keyfile=settings.SERVER_KEY_PATH,
    )
    # uvicorn.run(app, host="0.0.0.0", port=15000)

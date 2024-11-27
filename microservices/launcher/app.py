import logging
from fastapi import FastAPI
from routers import launch
from utils import utils
from dependencies.deps import get_configs

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

utils.set_env()
settings = get_configs()

app = FastAPI()

app.include_router(launch.router, prefix="/launcher", tags=["launcher"])

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
        port=15003,
        # reload=True,
        ssl_certfile=settings.SERVER_CERT_PATH,
        ssl_keyfile=settings.SERVER_KEY_PATH,
    )

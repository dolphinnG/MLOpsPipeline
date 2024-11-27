import logging
from fastapi import FastAPI
from routers import distributed_jobs_monitor
from dependencies.deps import get_settings
from middlewares.ExceptionHandlingMiddleware import ExceptionHandlingMiddleware
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

settings = get_settings()

app = FastAPI()

app.include_router(distributed_jobs_monitor.router, prefix="/distributed")
app.add_middleware(ExceptionHandlingMiddleware)

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
        port=15002,
        # reload=True,
        ssl_certfile=settings.SERVER_CERT_PATH,
        ssl_keyfile=settings.SERVER_KEY_PATH,
    )

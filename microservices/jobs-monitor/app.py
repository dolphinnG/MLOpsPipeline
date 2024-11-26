import logging
from fastapi import FastAPI
from routers import distributed_jobs_monitor
from dependencies.deps import get_settings
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

settings = get_settings()

app = FastAPI()

app.include_router(distributed_jobs_monitor.router, prefix="/distributed")

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

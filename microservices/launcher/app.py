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

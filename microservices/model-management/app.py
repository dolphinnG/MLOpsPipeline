import logging
from fastapi import FastAPI
from routers import mlflow
from dependencies.deps import get_settings
from utils.utils import set_env

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

set_env()
settings = get_settings()

app = FastAPI()
app.include_router(mlflow.router, prefix="/mlflow")
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run('app:app', host="localhost", port=15000, reload=True, ssl_certfile=settings.SERVER_CERT_PATH, ssl_keyfile=settings.SERVER_KEY_PATH)
    uvicorn.run(app, host="0.0.0.0", port=15000)

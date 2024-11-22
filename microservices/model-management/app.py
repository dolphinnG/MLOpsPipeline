import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import mlflow

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()
app.include_router(mlflow.router, prefix="/mlflow")
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app:app', host="localhost", port=15000, reload=True)

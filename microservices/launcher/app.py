import logging
from fastapi import FastAPI
from routers import launch

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()

app.include_router(launch.router, prefix="/launcher", tags=["launcher"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('app:app', host="localhost", port=15003, reload=True)
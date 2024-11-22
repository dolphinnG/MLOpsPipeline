import logging
from fastapi import FastAPI
from routers import distributed_jobs_monitor

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()

app.include_router(distributed_jobs_monitor.router, prefix="/distributed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app:app', host="localhost", port=15002, reload=True, ssl_certfile="dolphin.rootCA.crt", ssl_keyfile="dolphin.rootCA.key")
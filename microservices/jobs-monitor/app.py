from fastapi import FastAPI
from routers import distributed_jobs_monitor

app = FastAPI()

app.include_router(distributed_jobs_monitor.router, prefix="/distributed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app:app', host="localhost", port=15002, reload=True)
from fastapi import FastAPI
from routers import launch

app = FastAPI()

app.include_router(launch.router, prefix="/launcher", tags=["launcher"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('app:app', host="localhost", port=15003, reload=True)
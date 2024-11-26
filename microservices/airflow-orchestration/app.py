from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from routers.dag_router import dag_router
from routers.dag_run_router import dag_run_router
from routers.task_instance_router import task_instance_router
from dependencies.deps import get_settings

settings = get_settings()

app = FastAPI()

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": "Operation failed", "details": str(exc)},
    )


# Include routers in the FastAPI app
app.include_router(dag_router, prefix="/api/v1")
app.include_router(dag_run_router, prefix="/api/v1")
app.include_router(task_instance_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=15001,
        # reload=True,
        ssl_certfile=settings.SERVER_CERT_PATH,
        ssl_keyfile=settings.SERVER_KEY_PATH,
    )

# configuration = client.Configuration(host="http://localhost:8080/api/v1", username="user", password="bitnami")

# # Enter a context with an instance of the API client
# with client.ApiClient(configuration) as api_client:
#     # Create an instance of the config API class
#     api_instance = config_api.ConfigApi(api_client)

#     try:
#         # Get current configuration
#         api_response = api_instance.get_config()
#         pprint(api_response)
#     except client.ApiException as e:
#         print("Exception when calling ConfigApi->get_config: %s\n" % e)

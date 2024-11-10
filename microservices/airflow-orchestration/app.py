from fastapi import FastAPI
from routers.dag_router import dag_router
from routers.dag_run_router import dag_run_router
from routers.task_instance_router import task_instance_router

app = FastAPI()

# Include routers in the FastAPI app
app.include_router(dag_router, prefix="/api/v1")
app.include_router(dag_run_router, prefix="/api/v1")
app.include_router(task_instance_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=9999, reload=True)

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
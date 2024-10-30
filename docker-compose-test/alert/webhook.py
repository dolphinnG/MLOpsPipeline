from fastapi import FastAPI, Request
import uvicorn
import requests
from prometheus_client import Gauge, generate_latest, REGISTRY
from prometheus_client.exposition import start_http_server

app = FastAPI()

# Define the Gauge metric
model_drifted_total = Gauge('model_drifted_total', 'Total number of model drifts detected', ['model'])

# Start the Prometheus metrics server
start_http_server(8001)


### we should just let the metric start from 0 again if the app got restarted. 
# No need to reinitialize the metric to last known value

# def initialize_metrics(): 
#     prometheus_url = 'http://127.0.0.1:9090/api/v1/query'
#     query = 'model_drifted_total'
#     response = requests.get(prometheus_url, params={'query': query})
#     data = response.json()

#     if data['status'] == 'success':
#         for result in data['data']['result']:
#             model = result['metric']['model']
#             value = float(result['value'][1])
#             model_drifted_total.labels(model=model).set(value)

# @app.on_event("startup")
# async def startup_event():
#     initialize_metrics()

@app.post("/alert")
async def alert(request: Request):
    alert_data = await request.json()
    print("Alert received:", alert_data)
    
    # Process the alert data
    for alert in alert_data.get("alerts", []):
        model = alert["labels"].get("model")
        if model:
            print(f"Alert for model {model}")
    
    return {"message": "Alert received", "data": alert_data}

@app.get("/increment/{model_name}")
async def increment_metric(model_name: str):
    model_drifted_total.labels(model=model_name).inc()
    return {"message": f"Incremented model_drifted_total for model {model_name}"}

@app.get("/reset/{model_name}")
async def reset_metric(model_name: str):
    model_drifted_total.labels(model=model_name).set(0)
    return {"message": f"Reset model_drifted_total for model {model_name}"}

@app.get("/metrics")
async def metrics():
    return generate_latest(REGISTRY)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
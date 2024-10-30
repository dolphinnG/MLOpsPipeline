# Install dependencies
# pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-exporter-prometheus

import datetime
from fastapi import FastAPI, Request
from loguru import logger
from opentelemetry import trace, metrics, propagate
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import httpx
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry import propagate
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import requests

# remember to set otel resources
app = FastAPI()

# Configure loguru
logger.add(
    "logs/app2/file_{time}.log", rotation="1 day", retention="7 days", level="DEBUG"
)

# Define resource with service.name
resource = Resource(attributes={"service.name": "my-fastapi-service/app3"})

# configure tracer provider
otlp_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4317", insecure=True)
# otlp_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
provider = TracerProvider(resource=resource)
provider.add_span_processor(span_processor)
trace.set_tracer_provider(provider)
# trace.get_tracer_provider().add_span_processor(span_processor)

#

# get a tracer instance
tracer = trace.get_tracer(__name__)

RequestsInstrumentor().instrument()

# configure metrics provider
otlp_exporter = OTLPMetricExporter(endpoint="http://127.0.0.1:4317", insecure=True)
# otlp_exporter = OTLPMetricExporter(endpoint="http://127.0.0.1:4318/v1/metrics")

metric_reader = PeriodicExportingMetricReader(exporter=otlp_exporter)
metrics.set_meter_provider(
    MeterProvider(metric_readers=[metric_reader], resource=resource)
)


# get a meter instance
meter = metrics.get_meter(__name__)
# Create a counter metric
request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    with tracer.start_as_current_span("log_requests") as span:
        span.add_event( # test span event, this will appear in the trace in the events tab of the span
            "nameeeee",
            {"attributeeeee": "valueeeee"},
            int(datetime.datetime.now().timestamp()),
        )
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        request_counter.add(
            1, {"method": request.method, "endpoint": str(request.url.path)}
        )
        return response


@app.get("/")
def read_root():
    with tracer.start_as_current_span("read_root"):
        logger.info("Handling root endpoint")
        logger.debug("Debug message")
        return {"message": "Welcome to FastAPI!"}


@app.get("/call_app2")
async def call_app2():
    with tracer.start_as_current_span("call_app2"):
        logger.info("Calling app2 endpoint")
        # response = await http_client.get("http://127.0.0.1:9998/")
        response = requests.get("http://127.0.0.1:9998/")
        logger.info(f"Response from app2: {response.status_code}")
        return response.json()


FastAPIInstrumentor.instrument_app(app)
http_client = httpx.AsyncClient()
HTTPXClientInstrumentor().instrument_client(http_client)

if __name__ == "__main__":
    import uvicorn

    # FastAPIInstrumentor.instrument_app(app)
    uvicorn.run(app, host="0.0.0.0", port=9997)

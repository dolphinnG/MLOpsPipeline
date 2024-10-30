from fastapi import FastAPI, Request
from loguru import logger
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Enum
from starlette.responses import Response

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

app = FastAPI() # USE PROMETHEUS CLIENT AND DEPRECATED JAEGER EXPORTER, KEEP HERE JUST FOR REFERENCE

# Configure loguru
logger.add("logs/app1/file_{time}.log", rotation="1 day", retention="7 days", level="DEBUG")

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
RESPONSE_COUNT = Counter('response_count', 'Total number of responses', ['status_code'])
e = Enum('my_state', 'The description of my state', states=['ok', 'error'])
e.state('ok')

# OpenTelemetry tracing
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "my-fastapi-service"
})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# # Configure OTLP exporter
# otlp_exporter = OTLPSpanExporter(
#     endpoint="localhost:14268",
#     insecure=True
# )
# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',
    agent_port=6831,
)
# Add the OTLP exporter to the tracer
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    logger.info(f"Request: {request.method} {request.url}")
    
    # Start a new span for the request
    with tracer.start_as_current_span("log_requests") as span:
        # Add attributes (tags) to the span
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.client_ip", request.client.host)

        response = await call_next(request)
        RESPONSE_COUNT.labels(status_code=response.status_code).inc()
        logger.info(f"Response status: {response.status_code}")

        # Add more attributes (tags) to the span
        span.set_attribute("http.status_code", response.status_code)
        # span.set_attribute("http.response_length", len(response.body))

    return response

@app.get("/")
def read_root():
    logger.info("Handling root endpoint")
    return {"message": "Welcome to FastAPI!"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
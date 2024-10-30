from fastapi import FastAPI
import logging
from logging.config import dictConfig
from opentelemetry import trace

# pip install opentelemetry-distro
# pip install opentelemetry-exporter-otlp
# log_config = {
#     "version": 1,
#     "formatters": {
#         "default": {
#             "format": "{asctime} {levelname} {name} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "default",
#         },
#     },
#     "root": {
#         "level": "INFO",
#         "handlers": ["console"],
#     },
# }

# dictConfig(log_config)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # still need to set this for OTEL to work
app = FastAPI()

@app.get("/")
def read_root():
    
    logger.info("Hello World infoooo")
    logger.debug("Hello World debug")
    logger.error("Hello World error")
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9991)


# $env:OTEL_PYTHON_LOG_LEVEL="debug"
# $env:OTEL_EXPORTER_OTLP_ENDPOINT="127.0.0.1:4317" 
# $env:OTEL_EXPORTER_OTLP_INSECURE="true"
# $env:OTEL_SERVICE_NAME="app4-test"
# $env:OTEL_METRICS_EXPORTER="none"
# $env:OTEL_TRACES_EXPORTER="otlp"
# $env:OTEL_LOGS_EXPORTER="otlp"
# $env:OTEL_PYTHON_LOG_CORRELATION="true"
# $env:OTEL_PYTHON_LOG_FORMAT="%(msg)s [span_id=%(span_id)s]"
# $env:OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"
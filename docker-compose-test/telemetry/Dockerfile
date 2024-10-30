# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app4 /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn opentelemetry-distro opentelemetry-exporter-otlp

# Make port 9991 available to the world outside this container
EXPOSE 9991

# Define environment variables
# ENV OTEL_PYTHON_LOG_LEVEL="debug"
# ENV OTEL_EXPORTER_OTLP_ENDPOINT="127.0.0.1:4317"
# ENV OTEL_EXPORTER_OTLP_INSECURE="true"
# ENV OTEL_SERVICE_NAME="app4-test"
# ENV OTEL_METRICS_EXPORTER="none"
# ENV OTEL_TRACES_EXPORTER=""
# ENV OTEL_LOGS_EXPORTER="console"
# ENV OTEL_PYTHON_LOG_CORRELATION="true"
# ENV OTEL_PYTHON_LOG_FORMAT="%(msg)s [span_id=%(span_id)s]"
# ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"

RUN opentelemetry-bootstrap -a install

# Run app.py when the container launches
CMD ["opentelemetry-instrument", "python", "app4.py"]
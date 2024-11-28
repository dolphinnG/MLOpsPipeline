# Use the official PyTorch image as the base image
FROM pytorch/pytorch:latest

# Set the working directory
WORKDIR /app

# Install Python packages
RUN pip install --no-cache-dir mlflow torchvision torchx[dev] torchx[kubernetes] boto3 psutil pynvml 

# Copy the application code
COPY . /app
# COPY ./MNIST /app/MNIST

# Set the entrypoint to keep the container running
ENTRYPOINT ["tail", "-f", "/dev/null"]
# Set environment variable for MLflow tracking URI
ENV MLFLOW_TRACKING_URI="https://mlflow-dolphin-service-tracking:443"
ENV MLFLOW_TRACKING_SERVER_CERT_PATH="/app/dolphin.rootCA.crt"
ENV MLFLOW_TRACKING_USERNAME="mlflow"
ENV MLFLOW_TRACKING_PASSWORD="mlflow"
ENV MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING="true"
ENV MLFLOW_TRACING_OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="http://otelcol-deploymentset-hehe-opentelemetry-collector:4317/v1/traces"
# # Command to run the application (optional, can be overridden)
# CMD ["python", "main.py"]

# supahakka/torchdpp-base:v5
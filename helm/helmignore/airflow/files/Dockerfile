FROM bitnami/airflow:latest

# Install torchx[dev] in the Airflow virtual environment
# RUN /opt/bitnami/airflow/venv/bin/pip install torchx[dev]
COPY ./r.txt /tmp/r.txt
RUN /opt/bitnami/airflow/venv/bin/pip install -r /tmp/r.txt



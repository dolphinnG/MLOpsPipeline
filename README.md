# MLOps Pipeline

## TODO: provide more detail to this README

## Overview: 
- MLOps Pipeline with integration of infrastructure for single-node/distributed training for traditional ML/Deep learnng/LLM. 
- Models are to be logged with mlflow, and deployed with Seldon.
- 1 single web UI to access every component (Airflow, Mlflow, ML training project launcher, Monitor UI for distributed jobs, UI for model deployment, UI for model inference (for testing convenivence only)).

Disclaimer: I do this solo, there is still much that could be improved upon the already implemented. Maybe i'll do when I have the energy
## Note:

This repository contains Ansible playbooks for automating the build, deployment, and undeployment of a cluster. 
**Disclaimer:** The installation of Kubernetes Custom Resource Definitions (CRDs) is not yet included in the playbook.

## Pipeline Diagrams
### Distributed training
![MLFlow Single Node](./zchart-drawio/images/mlflow-single-node.png)
![Torch DDP](./zchart-drawio/images/torchddp.png)
![Spark](./zchart-drawio/images/spark.png)
### Model Deployment
![Deployment](./zchart-drawio/images/deployment.png)
### Security architecture
![Security](./zchart-drawio/images/security.png)
### Telemetry architecture
![Telemetry](./zchart-drawio/images/telemetry.png)

## Future Implementations

1. Better integration of the pipeline with Airflow through Kafka.
2. Auto retrain and auto redeploy when alerted by Prometheus Alert Manager for model drift or outlier detection by models trained with this pipeline.
3. LLM LangGraph Agent to simplify model inference with the obscure V2 Open Inference protocol.

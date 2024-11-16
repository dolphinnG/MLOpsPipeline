#!/bin/bash

# Define the image and script to run
IMAGE="supahakka/launcher:v15"
MODULE="ddptest" # --m $MODULE 
SCRIPT="mlflowrun.py" # --script $SCRIPT

# Run the DDP training script with MLflow on Kubernetes
torchx run --scheduler kubernetes \
    --scheduler_args namespace=dolphin-ns,queue=default \
    --workspace="" \
    dist.ddp \
    --image $IMAGE \
    --name hehe \
    --cpu 1 \
    --m $MODULE \
    --rdzv_backend c10d \
    --rdzv_port 30303 \
    --j '2x2' \
    --env MLFLOW_S3_ENDPOINT_URL=http://mlflowtest-minio:80,MLFLOW_TRACKING_URI=http://mlflowtest-tracking:80,AWS_ACCESS_KEY_ID=admin,AWS_SECRET_ACCESS_KEY=admin123,MLFLOW_EXPERIMENT_NAME=topg \
    # --debug true
    # --max_retries 3 \ volcano does not support retrying


# export KUBECONFIG=/mnt/host-folder/config



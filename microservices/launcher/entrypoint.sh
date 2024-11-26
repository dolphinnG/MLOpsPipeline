#!/bin/bash

if [ "$IS_ON_K8S" = "true" ]; then
    python generate_kubeconfig.py
fi
# Run spark-con.sh script
./spark-conf-generation-script.sh


# Run app.py when the container launches
exec opentelemetry-instrument python app.py
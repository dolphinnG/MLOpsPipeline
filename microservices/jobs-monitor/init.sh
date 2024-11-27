#!/bin/bash

# export PATH=$PATH:$(pwd)
python generate_kubeconfig.py

opentelemetry-instrument python app.py
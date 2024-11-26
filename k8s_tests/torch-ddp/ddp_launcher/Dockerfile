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

# # Command to run the application (optional, can be overridden)
# CMD ["python", "main.py"]
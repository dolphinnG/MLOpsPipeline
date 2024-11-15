import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import mlflow
import mlflow.pytorch
import logging
from mlflow.models.signature import infer_signature
import pandas as pd

# # Set the number of OpenMP threads
# os.environ["OMP_NUM_THREADS"] = "4"  # Adjust this value based on your system's CPU capacity

# # Disable address-to-line conversion for stack traces
# os.environ["TORCH_DISABLE_ADDR2LINE"] = "1"

# os.environ["CUDA_VISIBLE_DEVICES"]=""


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define a simple model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(28 * 28, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        return self.fc(x)

# Training function
def train(rank, world_size):
    
    logger.info(f"Initializing process group with rank {rank} and world size {world_size}")
    # Initialize the process group
    dist.init_process_group("gloo", rank=rank, world_size=world_size)
    logger.info(f"mlflow s3 endpoint: {os.environ['MLFLOW_S3_ENDPOINT_URL']}")
    logger.info(f"mlflow tracking uri: {os.environ['MLFLOW_TRACKING_URI']}")
    logger.info(f"mlflow aws id: {os.environ['AWS_ACCESS_KEY_ID']}")
    logger.info(f"mlflow aws secret: {os.environ['AWS_SECRET_ACCESS_KEY']}")
    logger.info(f"mlflow experiment: {os.environ['MLFLOW_EXPERIMENT_NAME']}")
        
    # Determine the device to use (GPU or CPU)
    if torch.cuda.is_available():
        device = torch.device(f'cuda:{rank}')
        device_ids = [rank]
    else:
        device = torch.device('cpu')
        device_ids = None
    
    # hardcoding device to cpu for testing on non-gpu machines
    device = torch.device('cpu')
    device_ids = None
    logger.info(f"Using device: {device}")
    
    # Set up the model, loss function, and optimizer
    model = SimpleModel().to(device)
    ddp_model = DDP(model, device_ids=device_ids)
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.01)
    
    # Set up the data loader
    transform = transforms.Compose([transforms.ToTensor()])
    # YAN LECUN MNIST URL IS DOWN, AND SO ARE ALL THE MIRRORS, THIS DOWNLOAD WILL RETURN 403, 
    # TODO: CHANGE TO A LOCAL COPY OF THE DATASET FOR THIS DEMO
    dataset = datasets.MNIST('.', train=True, download=True, transform=transform)
    sampler = torch.utils.data.DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, sampler=sampler)
    
    # Start MLflow run
    if rank == 0:
        # os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://mlflowtest-minio:80"
        # os.environ['AWS_ACCESS_KEY_ID'] = "admin"
        # os.environ['AWS_SECRET_ACCESS_KEY'] = "admin123"
        # mlflow.set_tracking_uri("http://mlflowtest-tracking:80")
        
        # mlflow.set_experiment(os.environ['MLFLOW_EXPERIMENT_NAME'])
        mlflow.start_run()
        logger.info("Started MLflow run")
    
    # Training loop
    for epoch in range(2):
        ddp_model.train()
        epoch_loss = 0.0
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = ddp_model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        
        # Log metrics with MLflow
        if rank == 0:
            mlflow.log_metric("loss", epoch_loss / len(dataloader), step=epoch)
            logger.info(f"Epoch {epoch}, Loss: {epoch_loss / len(dataloader)}")
    
    # Save the model with MLflow
    if rank == 0:
        # Create an input example and infer the model signature
        input_example = torch.randn(1, 1, 28, 28).to(device)
        signature = infer_signature(input_example.cpu().numpy(), model(input_example).cpu().detach().numpy())
        
        model_info = mlflow.pytorch.log_model(ddp_model.module, "model", signature=signature, input_example=input_example.cpu().numpy())
        logger.info(f"Model saved with MLflow, model_uri: {model_info.model_uri}")

        # End MLflow run
        mlflow.end_run()
        logger.info("Ended MLflow run")

        pyfunc_model = mlflow.pyfunc.load_model(model_info.model_uri)
        test_input = input_example.cpu().numpy().reshape(1, 1, 28, 28)
        predictions = pyfunc_model.predict(test_input)
        logger.info(f"Model predictions: {predictions}")
        
    # Clean up
    logger.info(f"MASTER_ADDR: {os.environ['MASTER_ADDR']}, MASTER_PORT: {os.environ['MASTER_PORT']}")
    dist.destroy_process_group()
    logger.info(f"Destroyed process group for rank {rank}")

# Main function
def main():
    world_size = int(os.environ['WORLD_SIZE'])
    rank = int(os.environ['RANK'])
    # os.environ['MASTER_ADDR'] = os.environ['MASTER_ADDR']
    # os.environ['MASTER_PORT'] = os.environ['MASTER_PORT']
        
    logger.info(f"Starting training with rank {rank} and world size {world_size}")
    logger.info(f"MASTER_ADDR: {os.environ['MASTER_ADDR']}, MASTER_PORT: {os.environ['MASTER_PORT']}")
    train(rank, world_size)
    

if __name__ == "__main__":
    main()
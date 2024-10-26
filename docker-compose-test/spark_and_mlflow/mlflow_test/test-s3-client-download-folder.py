import os
import boto3
import mlflow.pyfunc

def create_minio_client(endpoint_url, access_key, secret_key):
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    return s3_client

def download_folder(s3_client, bucket_name, folder_uri, download_path):
    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # List all objects in the folder
    objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_uri)
    
    for obj in objects.get('Contents', []):
        key = obj['Key']
        # Remove the folder prefix from the key to get the relative path
        relative_path = os.path.relpath(key, folder_uri)
        local_file_path = os.path.join(download_path, relative_path)
        
        # Ensure the local directory exists
        local_dir = os.path.dirname(local_file_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        
        # Download the file
        s3_client.download_file(bucket_name, key, local_file_path)
        print(f"Downloaded {key} to {local_file_path}")

def load_model(model_path):
    model = mlflow.pyfunc.load_model(model_path)
    print("Model loaded successfully")
    return model

# Example usage
if __name__ == "__main__":
    endpoint_url = 'http://127.0.0.1:9900'  # Replace with your MinIO endpoint
    access_key = 'minio_user'
    secret_key = 'minio_password'
    bucket_name = 'mlflow'  # Replace with your bucket name
    folder_uri = "1/0676263b29ba4567981b72d64ffe2b85/artifacts/random_forest_model"
    download_path = 'downloaded'  # Local path to save the downloaded folder

    client = create_minio_client(endpoint_url, access_key, secret_key)
    print("MinIO client created successfully")
    
    download_folder(client, bucket_name, folder_uri, download_path)
    
    # Load the downloaded model
    model = load_model(os.path.join(download_path, 'model.pkl'))
    
    # Example input data for prediction
    import numpy as np
    input_data = np.array([
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [6.2, 3.4, 5.4, 2.3],
        [5.9, 3.0, 5.1, 1.8]
    ]).astype(np.float64)
    
    # Predict using the loaded model
    predictions = model.predict(input_data)
    print("Predictions:", predictions)
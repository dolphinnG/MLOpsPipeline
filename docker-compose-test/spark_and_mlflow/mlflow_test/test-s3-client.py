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

def download_model(s3_client, bucket_name, model_uri, download_path):
    s3_client.download_file(bucket_name, model_uri, download_path)
    print(f"Model downloaded successfully to {download_path}")

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
    model_uri = "1/0676263b29ba4567981b72d64ffe2b85/artifacts/random_forest_model/model.pkl"
    download_path = 'model.pkl'  # Local path to save the downloaded model

    client = create_minio_client(endpoint_url, access_key, secret_key)
    print("MinIO client created successfully")
    
    download_model(client, bucket_name, model_uri, download_path)
    
    # Load the downloaded model
    model = load_model(download_path)
    
    # Example input data for prediction
    import pandas as pd
    input_data = pd.DataFrame({
        'feature_0': [5.1, 4.9],
        'feature_1': [3.5, 3.0],
        'feature_2': [1.4, 1.4],
        'feature_3': [0.2, 0.2]
    })
    
    # Predict using the loaded model
    predictions = model.predict(input_data)
    print("Predictions:", predictions)

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    VOLCANO_NAMESPACE: str
    VOLCANO_QUEUE: str
    
    MLFLOW_TRACKING_URI: str
    MLFLOW_S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    
    S3_MINIO_ENDPOINT_NO_PATH: str
    
    REDIS_HOST: str 
    REDIS_PORT: int 
    REDIS_DB: int 
    REDIS_PASSWORD: str
        
    ROOT_CA_CERT_PATH: str
    
    SERVER_CERT_PATH: str
    SERVER_KEY_PATH: str
    
    MLFLOW_TRACKING_SERVER_CERT_PATH: str
    MLFLOW_TRACKING_USERNAME:str
    MLFLOW_TRACKING_PASSWORD:str
    MLFLOW_TRACING_OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: str
    
    model_config = SettingsConfigDict(
        env_file="env/.env", env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
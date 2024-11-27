from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    MLFLOW_TRACKING_URI: str
    MLFLOW_S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    
    ROOT_CA_CERT_PATH: str
    
    SERVER_CERT_PATH: str
    SERVER_KEY_PATH: str
    
    MLFLOW_TRACKING_SERVER_CERT_PATH: str
    MLFLOW_TRACKING_USERNAME:str
    MLFLOW_TRACKING_PASSWORD:str
    
    model_config = SettingsConfigDict(
        env_file="env/.env", env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
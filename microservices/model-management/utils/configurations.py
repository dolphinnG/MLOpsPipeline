from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    MLFLOW_TRACKING_URI: str
    MLFLOW_S3_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix=""
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
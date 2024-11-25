
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    SELDON_SCHEDULER_GRPC_ENDPOINT: str 
    SELDON_INFERENCE_GRPC_ENDPOINT: str 
    SELDON_DATAPLANE_GRPC_ENDPOINT: str 

    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
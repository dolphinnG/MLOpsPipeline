
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    AIRFLOW_API_ENDPOINT: str
    AIRFLOW_API_USER: str 
    AIRFLOW_API_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix=""
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
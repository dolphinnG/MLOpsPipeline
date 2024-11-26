
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    AIRFLOW_API_ENDPOINT: str
    AIRFLOW_API_USER: str 
    AIRFLOW_API_PASSWORD: str
    
    ROOT_CA_CERT_PATH: str
    
    SERVER_CERT_PATH: str
    SERVER_KEY_PATH: str

    
    model_config = SettingsConfigDict(
        env_file="env/.env", env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
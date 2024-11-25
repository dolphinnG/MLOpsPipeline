
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Conf(BaseSettings):
    
    VOLCANO_NAMESPACE: str
    VOLCANO_QUEUE: str
    
    SPARK_MASTER_URL_WEB: str

    ROOT_CA_CERT_PATH:str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="", extra="ignore"
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
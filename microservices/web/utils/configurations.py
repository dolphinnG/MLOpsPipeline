from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Conf(BaseSettings):
    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_REALM_NAME: str
    KEYCLOAK_REDIRECT_URI: str
    KEYCLOAK_TOKEN_AUDIENCE: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    LDAP_SERVER_URL: str
    LDAP_ADMIN_DN: str
    LDAP_ADMIN_PASSWORD: str
    # LDAP_PORT: int
    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix=""
    )
    # model_config = SettingsConfigDict(secrets_dir='/run/secrets')


# Create an instance of the settings
# settings = Conf()
# print(settings)
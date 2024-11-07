from fastapi.templating import Jinja2Templates
from keycloak import KeycloakOpenID
from functools import lru_cache
from services.implementations.RedisCacheService import RedisService
from services.interfaces.ICacheService import ICacheService
from utils.configurations import Conf


@lru_cache
def get_configurations():
    return Conf()  # type: ignore


configs = get_configurations()


# Dependency function to get the templates object
def get_templates():
    return Jinja2Templates(directory="templates")


kc = KeycloakOpenID(
    server_url=configs.KEYCLOAK_SERVER_URL,
    realm_name=configs.KEYCLOAK_REALM_NAME,
    client_id=configs.KEYCLOAK_CLIENT_ID,
    client_secret_key=configs.KEYCLOAK_CLIENT_SECRET,
)


def get_keycloak_openid():
    return kc


cache_service = RedisService(
    configs.REDIS_HOST, configs.REDIS_PORT, configs.REDIS_DB
)

# Dependency function to get the cache service
def get_cache_service() -> ICacheService:
    return cache_service

# def get_auth_service():
#     from services.authService import AuthService
#     return AuthService.get_instance()

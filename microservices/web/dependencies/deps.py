from fastapi.templating import Jinja2Templates
import httpx
from keycloak import KeycloakOpenID
from functools import lru_cache
from services.implementations.LDAPService import LDAPService
from services.implementations.RedisCacheService import RedisService
from services.interfaces.ICacheService import ICacheService
from services.interfaces.IUserService import IUserService
from utils.configurations import Conf


@lru_cache
def get_configurations() -> Conf:
    return Conf()  # type: ignore

configs = get_configurations()

# Dependency function to get the templates object
@lru_cache
def get_templates():
    return Jinja2Templates(directory="templates")


@lru_cache
def get_keycloak_openid():
    return KeycloakOpenID(
        server_url=configs.KEYCLOAK_SERVER_URL,
        realm_name=configs.KEYCLOAK_REALM_NAME,
        client_id=configs.KEYCLOAK_CLIENT_ID,
        client_secret_key=configs.KEYCLOAK_CLIENT_SECRET,
        verify=configs.ROOT_CA_CERT_PATH,  # type: ignore # wack typehint lmao
    )


# Dependency function to get the cache service
@lru_cache
def get_cache_service() -> ICacheService:
    return RedisService(
        configs.REDIS_HOST,
        configs.REDIS_PORT,
        configs.REDIS_DB,
        configs.REDIS_PASSWORD,
        configs.ROOT_CA_CERT_PATH,
        True,
    )


async def get_ldap_service() -> IUserService:
    ldap_server = configs.LDAP_SERVER_URL
    admin_dn = configs.LDAP_ADMIN_DN
    admin_password = configs.LDAP_ADMIN_PASSWORD

    return LDAPService(ldap_server, admin_dn, admin_password, configs.ROOT_CA_CERT_PATH)


@lru_cache
def get_httpx_async_client():
    return httpx.AsyncClient(
        follow_redirects=True, timeout=100.0, verify=configs.ROOT_CA_CERT_PATH
    )


from functools import lru_cache
import httpx
from services.VolcanoFacade import VolcanoFacade
from utils.configurations import Conf


@lru_cache
def get_settings():
    return Conf() # type: ignore

settings = get_settings()

@lru_cache
def get_volcano_service():
    return VolcanoFacade(settings.VOLCANO_NAMESPACE, settings.VOLCANO_QUEUE)

@lru_cache
def get_httpx_async_client():
    return httpx.AsyncClient(follow_redirects=True)
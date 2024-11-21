
from functools import lru_cache
import httpx


@lru_cache
def get_httpx_async_client():
    return httpx.AsyncClient(follow_redirects=True)
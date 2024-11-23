from functools import lru_cache
from services.AirflowService import AirflowFacade
from utils.configurations import Conf

settings = Conf()  # type: ignore

 
@lru_cache
def get_airflow_facade() -> AirflowFacade:
    return AirflowFacade(
        host=settings.AIRFLOW_API_ENDPOINT,
        username=settings.AIRFLOW_API_USER,
        password=settings.AIRFLOW_API_PASSWORD,
        ssl_ca_cert=settings.ROOT_CA_CERT_PATH,
    )

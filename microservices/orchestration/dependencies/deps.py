
from services.AirflowService import AirflowFacade

def get_airflow_facade() -> AirflowFacade:
    return AirflowFacade(host="http://localhost:8080/api/v1", username="user", password="bitnami")

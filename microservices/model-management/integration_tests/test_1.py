
from mlflow import MlflowClient
from mlflow.entities.view_type import ViewType

from integration_tests.A import A



# arrange, act, assert

def test_mlflowClient_search_runs_id2_have_length_8():
    # arrange
    client = MlflowClient(tracking_uri="http://127.0.0.1:5000")
    a = A()
    # act
    runs = client.search_runs(experiment_ids=["2"])
    # assert
    assert len(runs) == 8

import logging
import pandas as pd
from typing import Dict
from mlflow.pyfunc.model import PythonModel
from mlflow.models import set_model
import mlflow.pyfunc
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput, TensorData

logger = logging.getLogger(__name__)


class WrapperModel(PythonModel):

    def load_context(self, context):
        logged_model = context.artifacts["inner_spark_model"] # testspark5.py
        # NOTE: THIS PYFUNC LOADING NEEDS MINIO CREDENTIALS TO WORK, 
        # CURRENTLY HARDCODED IN THE ENV OF THE DOCKERFILE OF CUSTOM SELDON MLSERVER FOR NOW, 
        # REMEMBER TO EXTRACT AND USE K8S SECRET IN THE FUTURE
        self._sparkModel = mlflow.pyfunc.load_model(logged_model) 

    def predict(self, context, model_input, params):

        print("MODEL_INPUT: " + str(model_input))

        # model_input: InferenceRequest  # MLflow v2 protocol models receives an InferenceRequest in model_input
        # input = model_input.inputs[0]
        # name = input.name
        # data = input.data.root
        # dic = {name: [data]}
        # print("DIC: " + str(dic))

        dic = model_input
        dic['features'] = dic['features'].tolist()
        print("DIC: " + str(dic))
        pandas_df = pd.DataFrame(dic)
        print("PANDAS_DF: " + str(pandas_df))
        
        # Use the Spark model to make predictions
        res = self._sparkModel.predict(pandas_df)
        
        # logger.log(logging.INFO, "RESULT: " + str(res))
        print("RESULT: " + str(res))
        
        # NOTE: MLFLOW v2 models return a TensorDict = Dict[str, np.ndarray]
        return {"whateverhere": res[0].values}
        


# Specify which definition in this script represents the model instance
set_model(WrapperModel())

"""

signature:
  inputs: '[{"name": "features", "type": "tensor", "tensor-spec": {"dtype": "float64",
    "shape": [1, 2]}}]'
  outputs: '[{"name": "whateverhere", "type": "tensor", "tensor-spec": {"dtype": "float64",
    "shape": [1, 2]}}]'

curl -v http://seldon-mesh:80/v2/models/model-from-code/infer \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": [
             {
               "name": "features",
               "shape": [1, 2],
               "datatype": "FP64",
               "data": [[2.0, 3.6]]
             }
           ]
         }'
SINCE WE DONT INCLUDE A MODEL SIGNATURE, SELDON WON'T BLOCK THE LOADING OF THE MODEL
BUT THAT MEANS WE MUST OURSELVES COORDINATE THE USER'S REQUEST AND THE WAY THE WRAPPER MODEL 
CONVERT THE INPUT INTO THE FORMAT THE WRAPPED (SPARK) MODEL EXPECTS

BASICALLY, BY LOADING THE OG MODEL WITH MLFLOW PYFUNC, AND PROVIDING ANOTHER MLFLOW PYFUNC WRAPPER TO 
BE DEPLOYED TO SELDON, WE CAN NOW DEPLOY ANY TYPE OF MLFLOW MODEL TO SELDON DESPITE THE FACT THAT
SELDON SUPPORT FOR MLFLOW IS KINDA WACK LMAO. 

NOTE: WE CAN NOW DEPLOY MLFLOW MODEL FROM CODE THIS WAY, MEANING LANGCHAIN, OPENAI LLM, ETC.
"""

# curl -v http://seldon-mesh:80/v2/models/model-from-code/infer \
#      -H "Content-Type: application/json" \
#      -d '{
#            "inputs": [
#              {
#                "name": "features",
#                "shape": [2],
#                "datatype": "FP64",
#                "data": [2.0, 3.6]
#              }
#            ]
#          }'
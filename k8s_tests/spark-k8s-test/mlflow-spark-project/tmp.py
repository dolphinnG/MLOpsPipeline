import mlflow
import pandas as pd
from pyspark.ml.linalg import Vectors
from pyspark.sql import SparkSession

# logged_model = 's3://mlflow/1/3cab96d2208b406d87591f1cecf35eb0/artifacts/model'
logged_model = 's3://mlflow/5/15181d5c31e84b12a4a8746dfed93d2f/artifacts/model'


# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Example data similar to test_df
data = {

    "features": [[41.0, 663.6]]
}

# Create a pandas DataFrame
pandas_df = pd.DataFrame(data)
print(pandas_df)
# Make predictions
r = loaded_model.predict(pandas_df)
print(r)

# data = {

#     "features": [[41.0, 663.6]]
# }

# logged_modelfromcode = 's3://mlflow/6/15f64c4771204e54a9a9fc999528566e/artifacts/spark-modelfromcode'
# # Load model as a PyFuncModel.
# loaded_model = mlflow.pyfunc.load_model(logged_modelfromcode)
# res = loaded_model.predict(data)
# print(res)

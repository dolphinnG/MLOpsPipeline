import mlflow
import pandas as pd
from pyspark.ml.linalg import Vectors

logged_model = 's3://mlflow/1/3cab96d2208b406d87591f1cecf35eb0/artifacts/model'

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



curl -v http://seldon-mesh:80/v2/models/torch-ddp/infer \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": [
             {
               "name": "input-0",
               "shape": [-1,1,28,28],
               "datatype": "FP32",
               "data": [],
               "parameters": {
                 "content_type": "np"
               }
             }
           ]
         }'



cat <<EOF > generate_request.py
import numpy as np
import json
import requests

# Generate 28x28 array of random numbers between 0 and 250
random_data = np.random.randint(0, 251, (28, 28)).tolist()

# Create the payload
payload = {
    "inputs": [
        {
            "name": "input-0",
            "shape": [-1, 1, 28, 28],
            "datatype": "FP32",
            "data": random_data,
            "parameters": {
                "content_type": "np"
            }
        }
    ]
}

# Convert payload to JSON string
payload_json = json.dumps(payload)

# Make the POST request
response = requests.post(
    "http://seldon-mesh:80/v2/models/torch-ddp/infer",
    headers={"Content-Type": "application/json"},
    data=payload_json
)

# Print the response
print(response.text)
EOF
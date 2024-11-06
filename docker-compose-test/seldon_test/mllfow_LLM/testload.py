
import requests

url = "http://127.0.0.1:5555/invocations"
headers = {
    "Content-Type": "application/json"
}
data = {
    "inputs": [
        {
            "name": "input-0",
            "datatype": "BYTES",
            "shape": [1],
            "data": ["your-string-input".encode('utf-8').decode('latin1')],
            "parameters": {
                "content_type": "str"
            }
        }
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
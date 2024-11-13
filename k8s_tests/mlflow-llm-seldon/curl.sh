curl -v http://seldon-mesh:80/v2/models/llm-model/infer \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": [
             {
               "name": "language",
               "shape": [-1,2],
               "datatype": "BYTES",
               "data": ["vietnamese", "japanese"]
             },
             {
               "name": "text",
               "shape": [-1,2],
               "datatype": "BYTES",
               "data": ["fuck you bitch"]
             }
           ]
         }'


curl -v http://seldon-mesh:80/v2/models/llm-model-openai-2/infer \
     -H "Content-Type: application/json" \
     -d '{
           "parameters": {
             "max_tokens": 500,
             "temperature": 0
           },
           "inputs": [
             {
               "name": "lmaohehe",
               "shape": [-1,1],
               "datatype": "BYTES",
               "data": ["I tried so hard and get so near, but in the end it doesnt even good"]
             }
           ]
         }'

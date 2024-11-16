seldon model infer iris \
  '{"inputs": [{"name": "predict", "shape": [3, 5], "datatype": "FP32", "data": [1,2,3,4,5,6,7,8,0,0,0,0,1,2,3] }]}' 


seldon model infer tfsimple1 \
    '{"inputs":[{"name":"INPUT0","data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"datatype":"INT32","shape":[2,16]},{"name":"INPUT1","data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"datatype":"INT32","shape":[2,16]}]}' | jq -M .





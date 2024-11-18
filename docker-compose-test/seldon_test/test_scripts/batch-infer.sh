seldon model infer irisreal  \
  '{"inputs": [{"name": "predict", "shape": [1, 4], "datatype": "FP32", "data": [[1, 2, 3, 4]]}]}'

seldon model infer iris2 \
        --inference-mode grpc \
        '{"model_name":"iris","inputs":[{"name":"input","contents":{"fp32_contents":[1,2,3,4]},"datatype":"FP32","shape":[1,4]}]}'

seldon model infer tfsimple1 \
    '{"inputs":[{"name":"INPUT0","data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"datatype":"INT32","shape":[2,16]},{"name":"INPUT1","data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"datatype":"INT32","shape":[2,16]}]}' | jq -M .

grpcurl \
    -d '{"model_name":"iris2","inputs":[{"name":"input","contents":{"fp32_contents":[1,2,3,4]},"datatype":"FP32","shape":[1,4]}]}' \
    -plaintext \
    -import-path /home/dolphin/Desktop/pipeline/MLOpsPipeline/docker-compose-test/seldon_test/test_scripts \
    -proto v2_dataplane.proto \
    -rpc-header seldon-model:iris2 \
    0.0.0.0:9000 inference.GRPCInferenceService/ModelInfer

seldon pipeline infer testpipeline \
    '{"inputs":[{"name":"INPUT0","data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"datatype":"INT32","shape":[1,16]},{"name":"INPUT1","data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"datatype":"INT32","shape":[1,16]}]}' | jq -M .


grpcurl -d '{"model":{"meta":{"name":"irishaha"},"modelSpec":{"uri":"gs://seldon-models/mlserver/iris","requirements":["sklearn"],"memoryBytes":500},"deploymentSpec":{"replicas":1}}}' \
    -plaintext \
    -import-path /home/dolphin/Desktop/pipeline/MLOpsPipeline/docker-compose-test/seldon_test/test_scripts \
    -proto scheduler.proto \
    0.0.0.0:9004 seldon.mlops.scheduler.Scheduler/LoadModel
         
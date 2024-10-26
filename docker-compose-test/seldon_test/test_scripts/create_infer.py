from v2_dataplane_pb2 import InferTensorContents, ModelInferRequest, ModelInferResponse

# create a ModelInferRequest

input = ModelInferRequest.InferInputTensor(
    name = "predict",
    shape = [1,4],
    datatype="FP32",
    contents=InferTensorContents(
        fp32_contents=[1,2,3,4]
    )
)

model_req = ModelInferRequest(
    model_name="iris-model-test",
    id="dolphin1234",
    inputs=[input]
)

# output = ModelInferResponse.InferOutputTensor(
#     name = "predict",
#     shape = [1,4],
#     datatype="FP32",
#     contents=InferTensorContents(
#         fp32_contents=[1,2,3,4]
#     )
# )

# model_res = ModelInferResponse(
#     model_name="iris-model-test",
#     id="dolphin1234",
    
# )

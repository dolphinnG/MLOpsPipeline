import grpc
import scheduler_pb2
import scheduler_pb2_grpc

def run():
    # Step 2: Create a gRPC channel to the Seldon service
    channel = grpc.insecure_channel('127.0.0.1:9004')  # Replace with your server address
    
    # Step 3: Create a stub (client)
    stub = scheduler_pb2_grpc.SchedulerStub(channel)
    metadata = scheduler_pb2.MetaData(
        name = "iris-hehe",
        kind = "gasdgsd",
        version = "v1111"
    )
    model_spec = scheduler_pb2.ModelSpec(
        uri = "gs://seldon-models/scv2/samples/mlserver_1.6.0/iris-sklearn",
        requirements = ["sklearn"],
        memoryBytes=512
    )
    
    deployment_spec = scheduler_pb2.DeploymentSpec(
        replicas=1,
        minReplicas=1,
        maxReplicas=3,
        logPayloads=True,
    )
    
    stream_spec = scheduler_pb2.StreamSpec( # this is useless, has no effect lmao
        inputTopic="default-output-topic",
        outputTopic="default-input-topic",
    )
    
    model = scheduler_pb2.Model(
        meta=metadata,
        modelSpec=model_spec,
        deploymentSpec=deployment_spec,
        streamSpec=stream_spec    
    )
    # Step 4: Create a request
    request = scheduler_pb2.LoadModelRequest  (
        model = model
    )
    
    # Step 5: Make the call
    try:
        response = stub.LoadModel(request) 
        # response is always empty
        # call the ModelStatus method of stub to get the status of the model
        
        
        print("load model response:", response)
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
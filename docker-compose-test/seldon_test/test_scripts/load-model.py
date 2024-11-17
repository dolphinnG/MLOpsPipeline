import grpc
import scheduler_pb2
import scheduler_pb2_grpc

def create_channel_and_stub(server_address):
    # Create a gRPC channel to the Seldon service
    channel = grpc.insecure_channel(server_address)
    # Create a stub (client)
    stub = scheduler_pb2_grpc.SchedulerStub(channel)
    return channel, stub

def load_model(stub):
    metadata = scheduler_pb2.MetaData(
        name="iris-hehe",
        kind="gasdgsd",
        version="v1111"
    )
    model_spec = scheduler_pb2.ModelSpec(
        uri="gs://seldon-models/scv2/samples/mlserver_1.6.0/iris-sklearn",
        requirements=["sklearn"],
        memoryBytes=512
    )
    
    deployment_spec = scheduler_pb2.DeploymentSpec(
        replicas=1,
        minReplicas=1,
        maxReplicas=3,
        logPayloads=True,
    )
    
    stream_spec = scheduler_pb2.StreamSpec(
        inputTopic="default-output-topic",
        outputTopic="default-input-topic",
    )
    
    model = scheduler_pb2.Model(
        meta=metadata,
        modelSpec=model_spec,
        deploymentSpec=deployment_spec,
        streamSpec=stream_spec    
    )
    # Create a request
    request = scheduler_pb2.LoadModelRequest(
        model=model
    )
    
    # Make the call
    try:
        response = stub.LoadModel(request)
        print("load model response:", response)
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    server_address = '127.0.0.1:9004'  # Replace with your server address
    channel, stub = create_channel_and_stub(server_address)
    load_model(stub)

if __name__ == '__main__':
    main()
    

import grpc
import scheduler_pb2
import scheduler_pb2_grpc

def run():
    # Step 2: Create a gRPC channel to the Seldon service
    channel = grpc.insecure_channel('127.0.0.1:9004')  # Replace with your server address
    
    # Step 3: Create a stub (client)
    stub = scheduler_pb2_grpc.SchedulerStub(channel)
    model_ref = scheduler_pb2.ModelReference(
        name="iris",
        # version="your_model_version"
    )
    # Step 4: Create a request
    request = scheduler_pb2.UnloadModelRequest  (
        model = model_ref
    )
    
    # Step 5: Make the call
    try:
        response = stub.UnloadModel(request)
        # Process the response
        print("UnloadPipeline response:", response)
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")

if __name__ == '__main__':
    run()
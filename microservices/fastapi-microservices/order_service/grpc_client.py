import grpc
import user_pb2
import user_pb2_grpc

# Connect to the gRPC server
channel = grpc.insecure_channel("localhost:50051")
stub = user_pb2_grpc.UserServiceStub(channel)

# Send a request to the gRPC server
try:
    response = stub.GetUser(user_pb2.UserRequest(user_id=1))
    print(f"User ID: {response.id}, Username: {response.name}, Email: {response.email}")

except grpc.RpcError as e:
    print(f"gRPC Error: {e.code()} - {e.details()}")

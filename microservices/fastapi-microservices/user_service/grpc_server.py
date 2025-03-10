import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

# ✅ Sample database (Replace with actual DB later)
users = {
    1: {"id": 1, "username": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "username": "Bob", "email": "bob@example.com"},
}

# ✅ Define the gRPC Service
class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        """Handles incoming GetUser requests"""
        user = users.get(request.user_id)  # ✅ Fetch user data
        if user:
            return user_pb2.UserResponse(id=user["id"], name=user["username"], email=user["email"])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.UserResponse()  # ✅ Return empty response if user not found

# ✅ Start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # ✅ Create server with threading
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)  # ✅ Register service
    server.add_insecure_port("[::]:50051")  # ✅ Expose gRPC server on port 50051
    print("User Service gRPC server started on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()  # ✅ Start the server

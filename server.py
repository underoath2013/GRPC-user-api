import signal
import grpc
from grpc_reflection.v1alpha import reflection
import example_pb2
import example_pb2_grpc

from concurrent import futures


class UserServicer(example_pb2_grpc.UsersAPIServicer):
    users = dict()
    count = 1

    def CreateUser(self, request, context):
        e = {'name': request.name,
             'age': request.age}
        print(f'Add user: "{e}"')

        e['id'] = UserServicer.count
        UserServicer.count += 1

        UserServicer.users[e['id']] = e
        return example_pb2.CreateUserResponse(id=e['id'])

    def GetUser(self, request, context):
        print(f'Get user: id - "{request.id}"')
        if request.id not in UserServicer.users:
            raise grpc.RpcError(f'User with id "{request.id}" not exists')

        e = UserServicer.users[request.id]
        return example_pb2.GetUserResponse(
            id=e['id'], name=e['name'], age=e['age'])

    def DeleteUser(self, request, context):
        print(f'Remove user: id - "{request.id}"')
        if request.id not in UserServicer.users:
            raise grpc.RpcError(f'User with id "{request.id}" not exists')

        e = UserServicer.users.pop(request.id)
        UserServicer.count -= 1
        return example_pb2.DeleteUserResponse(id=e['id'])

    def UpdateUser(self, request, context):
        print(f'Update user: id - "{request.id}", name - "{request.name}", age - "{request.age}"')
        if request.id not in UserServicer.users:
            raise grpc.RpcError(f'User with id "{request.id}" not exists')

        UserServicer.users[request.id]['name'] = request.name
        UserServicer.users[request.id]['age'] = request.age

        return example_pb2.UpdateUserResponse(
            id=request.id, name=UserServicer.users[request.id]['name'], age=UserServicer.users[request.id]['age'])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_UsersAPIServicer_to_server(UserServicer(), server)

    def handle_sigint(sig, frame):
        print("Caught SIGINT, shutting down server...")
        server.stop(0)
    signal.signal(signal.SIGINT, handle_sigint)

    service_names = (
        example_pb2.DESCRIPTOR.services_by_name['UsersAPI'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server listening on :50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

import grpc
from example_pb2_grpc import UsersAPIStub
import example_pb2


channel = grpc.insecure_channel('localhost:50051')
stub = UsersAPIStub(channel)


def create_user(name, age):
    request = example_pb2.CreateUserRequest(name=name, age=age)
    return stub.Createuser(request)


def get_user(id_):
    request = example_pb2.GetUserRequest(id=id_)
    return stub.Getuser(request)


def delete_user(id_):
    request = example_pb2.DeleteUserRequest(id=id_)
    return stub.Deleteuser(request)


def update_user(id_, name, age):
    request = example_pb2.UpdateUserRequest(id=id_, name=name, age=age)
    return stub.Updateuser(request)

import grpc
import greeting_pb2
import greeting_pb2_grpc
from concurrent import futures

class GreeterServicer(greeting_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):

        name = request.name
        message = f"Hello,{name}!"
        return greeting_pb2.HelloResponse(message=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    greeting_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')

    print("Запуск сервера на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


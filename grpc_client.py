import grpc
import greeting_pb2
import greeting_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greeting_pb2_grpc.GreeterStub(channel)
        request = greeting_pb2.HelloRequest(name="Мир")
        response = stub.SayHello(request)
        print("Ответ сервера:", response.message)

if __name__ == '__main__':
    run()


import grpc

from clients.http.gateway.operations.operations_schema import MakeOperationRequestSchema
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest, \
    OpenDebitCardAccountResponse
from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import GetOperationReceiptRequest
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import MakeTopUpOperationRequest
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from contracts.services.operations.operation_pb2 import OperationStatus
from grpcio_open_debit_card_account import open_debit_card_account_request
from tools.fakers import fake

# Создаём gRPC-канал к сервисам, работающим на порту 9003
channel = grpc.insecure_channel("localhost:9003")

# Инициализируем stubs (gRPC-клиенты)
users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service = AccountsGatewayServiceStub(channel)
operations_gateway_service = OperationsGatewayServiceStub(channel)


# 1. Создаём нового пользователя
create_user_request = CreateUserRequest(
    email=fake.email(),
    last_name=fake.last_name(),
    first_name=fake.first_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)

create_user_response = users_gateway_service.CreateUser(create_user_request)

# 2. открытие дебетового счета
open_debit_card_request = OpenDebitCardAccountRequest(user_id=create_user_response.user.id)
open_debit_card_response: OpenDebitCardAccountResponse = accounts_gateway_service.OpenDebitCardAccount(open_debit_card_request)

# 3 Операция пополнения счета
make_top_up_operation_request = MakeTopUpOperationRequest(
    status=OperationStatus.OPERATION_STATUS_COMPLETED,
    amount=fake.amount(),
    card_id=open_debit_card_response.account.cards[0].id,
    account_id=open_debit_card_response.account.id
)
make_top_up_operation_response = operations_gateway_service.MakeTopUpOperation(make_top_up_operation_request)

# 4 Получение чека по операции
get_operation_receipt_request = GetOperationReceiptRequest(operation_id=make_top_up_operation_response.operation.id)
get_operation_receipt_response = operations_gateway_service.GetOperationReceipt(get_operation_receipt_request)

# 5 Логирование результата
print('Get operation receipt response: receipt', get_operation_receipt_response)
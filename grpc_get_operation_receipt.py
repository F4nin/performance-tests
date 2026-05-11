from time import sleep

from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.http.gateway.cards.client import build_cards_gateway_http_client
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client
from clients.http.gateway.users.users_schema import CreateUserResponseSchema, CreateUserRequestSchema

users_gateway_client = build_users_gateway_grpc_client()
create_user_response = users_gateway_client.create_user()
print(create_user_response)

cards_account_client = build_accounts_gateway_grpc_client()
open_credit_account = cards_account_client.open_credit_card_account(user_id=create_user_response.user.id)
print(open_credit_account)

operations_gateways_clients = build_operations_gateway_grpc_client()
make_purchase_operation_response = operations_gateways_clients.make_purchase_operation(open_credit_account.account.cards[0].id , open_credit_account.account.id)

print(make_purchase_operation_response.operation.id)
sleep(4)
operation_receipt_client = build_operations_gateway_grpc_client()
operation_receipt_response = operation_receipt_client.get_operation_receipt(make_purchase_operation_response.operation.id)
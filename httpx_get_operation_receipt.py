from time import sleep

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.cards.client import build_cards_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.users.users_schema import CreateUserResponseSchema, CreateUserRequestSchema

users_gateway_client = build_users_gateway_http_client()
user_request = CreateUserRequestSchema()
create_user_response = users_gateway_client.create_user(user_request)
print(create_user_response)

cards_account_client = build_accounts_gateway_http_client()
open_credit_account = cards_account_client.open_credit_card_account(user_id=create_user_response.user.id)
print(open_credit_account)

operations_gateways_clients = build_operations_gateway_http_client()
make_purchase_operation_response = operations_gateways_clients.make_purchase_operation(open_credit_account.account.cards[0].id , open_credit_account.account.id)

print(make_purchase_operation_response.operation.id)
sleep(10)
operation_receipt_client = build_operations_gateway_http_client()
operation_receipt_response = operation_receipt_client.get_operation_receipt(make_purchase_operation_response.operation.id)

#print(operation_receipt_response)

# import time
#
# import httpx
#
# create_user_payload = {
#     "email": f"user.{time.time()}@example.com",
#     "lastName": "string",
#     "firstName": "string",
#     "middleName": "string",
#     "phoneNumber": "string"
# }
# create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
# create_user_response_data = create_user_response.json()
#
# open_credit_card_account_payload = {
#     "userId": create_user_response_data["user"]["id"]
# }
# open_credit_card_account_response = httpx.post(
#     "http://localhost:8003/api/v1/accounts/open-credit-card-account",
#     json=open_credit_card_account_payload
# )
# open_credit_card_account_response_data = open_credit_card_account_response.json()
#
# make_purchase_operation_payload = {
#     "status": "IN_PROGRESS",
#     "amount": 77.99,
#     "cardId": open_credit_card_account_response_data["account"]["cards"][0]["id"],
#     "category": "taxi",
#     "accountId": open_credit_card_account_response_data["account"]["id"]
# }
# make_purchase_operation_response = httpx.post(
#     "http://localhost:8003/api/v1/operations/make-purchase-operation",
#     json=make_purchase_operation_payload
# )
# make_purchase_operation_response_data = make_purchase_operation_response.json()
#
# get_operation_receipt_response = httpx.get(
#     f"http://localhost:8003/api/v1/operations/operation-receipt/"
#     f"{make_purchase_operation_response_data['operation']['id']}"
# )
# get_operation_receipt_response_data = get_operation_receipt_response.json()
#
# print('Get operation receipt response:', get_operation_receipt_response_data)
# print('Get operation receipt status code:', get_operation_receipt_response.status_code)
#

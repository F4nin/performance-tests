from locust import User, task, between

from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_locust_grpc_client
from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class OpenDebitCardAccountScenarioUser(User):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)
    host = "localhost"

    users_gateway_client: UsersGatewayGRPCClient
    create_user_response: CreateUserResponse
    accounts_gateway_client: AccountsGatewayGRPCClient

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        self.accounts_gateway_client.open_debit_card_account(user_id=self.create_user_response.user.id)


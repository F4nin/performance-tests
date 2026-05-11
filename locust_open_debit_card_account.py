from locust import User, task, between

from clients.http.gateway.accounts.accounts_schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client
from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.users.users_schema import CreateUserResponseSchema
from tools.fakers import fake

class OpenDebitCardAccountScenarioUser(User):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)
    host = "localhost"

    users_gateway_client: UsersGatewayHTTPClient
    create_user_response: CreateUserResponseSchema
    accounts_gateway_client: AccountsGatewayHTTPClient

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        self.accounts_gateway_client.open_debit_card_account(user_id=self.create_user_response.user.id)


from locust import User, between, task

from clients.http.gateway.accounts.accounts_schema import OpenSavingsAccountResponseSchema, GetAccountsResponseSchema
from clients.http.gateway.locust import GatewayHTTPTaskSet
from clients.http.gateway.users.users_schema import CreateUserResponseSchema


class GetAccountsTaskSet(GatewayHTTPTaskSet):

    create_user_response: CreateUserResponseSchema | None = None
    # open_savings_account_response: OpenSavingsAccountResponseSchema | None = None
    # get_accounts_response: GetAccountsResponseSchema | None = None

    @task(2)
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        if self.create_user_response is None:
            return
        self.accounts_gateway_client.open_deposit_account(user_id=self.create_user_response.user.id)

    @task(6)
    def get_accounts(self):
        if self.create_user_response is None:
            return
        self.get_accounts_response = self.accounts_gateway_client.get_accounts(user_id=self.create_user_response.user.id)

class GetDocumentsScenarioUser(User):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 3)  # Имитируем паузы между выполнением сценариев
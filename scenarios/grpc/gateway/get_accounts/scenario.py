from locust import task, User, between

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from tools.user import LocustBaseUser


class GetAccountsTaskSet(GatewayGRPCTaskSet):
    create_user_response: CreateUserResponse | None = None

    @task(2)
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        if self.create_user_response is None:
            return
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(user_id=self.create_user_response.user.id)

    @task(6)
    def get_accounts(self):
        if self.create_user_response is None:
            return
        self.get_accounts_response = self.accounts_gateway_client.get_accounts(user_id=self.create_user_response.user.id)

class GetAccountsScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    tasks = [GetAccountsTaskSet]

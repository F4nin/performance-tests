from locust import task

from clients.http.gateway.accounts.accounts_schema import OpenDepositAccountResponseSchema, \
    OpenDebitCardAccountResponseSchema
from clients.http.gateway.cards.cards_schema import IssuePhysicalCardResponseSchema
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.users_schema import CreateUserResponseSchema
from tools.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает дебетового счёт.
    3. Выпускает физическую карту.

    Использует базовый GatewayHTTPSequentialTaskSet и уже созданных в нём API клиентов.
    """
    create_user_response: CreateUserResponseSchema | None = None
    open_debit_account_response: OpenDebitCardAccountResponseSchema | None = None


    @task
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Открываем дебетовый счёт для созданного пользователя.
        Проверяем, что предыдущий шаг был успешным.
        """
        if not self.create_user_response:
            return
        self.open_debit_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id)

    @task
    def issue_physical_card(self):
        if (not self.create_user_response) or (not self.open_debit_account_response):
            return
        self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_debit_account_response.account.id)

class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    tasks = [IssuePhysicalCardSequentialTaskSet]





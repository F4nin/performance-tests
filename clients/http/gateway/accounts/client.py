from httpx import Response, QueryParams

from clients.http.client import HttpClient
from clients.http.gateway.accounts.accounts_schema import GetAccountsQuerySchema, OpenDepositAccountRequestSchema, \
    OpenSavingsAccountRequestSchema, OpenDebitCardAccountRequestSchema, OpenCreditCardAccountRequestSchema
from clients.http.gateway.client import build_gateway_http_client
from tools.routes import APIRoutes


class AccountsGatewayHTTPClient(HttpClient):
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.
    """
    def get_accounts_api(self, query: GetAccountsQuerySchema) -> Response:
        """
        Выполняет GET-запрос на получение списка счетов пользователя.

        :param query: Словарь с параметрами запроса, например: {'userId': '123'}.
        :return: Объект httpx.Response с данными о счетах.
        """
        return self.get(f"{APIRoutes.ACCOUNTS}", params=QueryParams(**query))

    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.

        :param request: Словарь с userId.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.ACCOUNTS}/open-deposit-account", json=request.model_dump(by_alias=True))

    def open_savings_account_api(self, request: OpenSavingsAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.

        :param request: Словарь с userId.
        :return: Объект httpx.Response.
        """
        return self.post(f"{APIRoutes.ACCOUNTS}/open-savings-account", json=request.model_dump(by_alias=True))

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.

        :param request: Словарь с userId.
        :return: Объект httpx.Response.
        """
        return self.post(f"{APIRoutes.ACCOUNTS}/open-debit-card-account", json=request.model_dump(by_alias=True))

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.

        :param request: Словарь с userId.
        :return: Объект httpx.Response.
        """
        return self.post(f"{APIRoutes.ACCOUNTS}/open-credit-card-account", json=request.model_dump(by_alias=True))

def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """
    Функция создаёт экземпляр AccountsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AccountsGatewayHTTPClient.
    """
    return AccountsGatewayHTTPClient(client=build_gateway_http_client())

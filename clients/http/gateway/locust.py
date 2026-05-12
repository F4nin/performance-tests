from locust import TaskSet, SequentialTaskSet

from clients.http.gateway.users.client import build_users_gateway_locust_http_client, UsersGatewayHTTPClient
from clients.http.gateway.cards.client import build_cards_gateway_locust_http_client, CardsGatewayHTTPClient
from clients.http.gateway.accounts.client import build_accounts_gateway_locust_http_client, AccountsGatewayHTTPClient
from clients.http.gateway.operations.client import build_operations_gateway_locust_http_client, \
    OperationsGatewayHTTPClient
from clients.http.gateway.documents.client import build_documents_gateway_locust_http_client, DocumentsGatewayHTTPClient


class GatewayHTTPTaskSet(TaskSet):
    """
    Базовый TaskSet для HTTP-сценариев, работающих с http-gateway.

    Здесь создаются все необходимые API клиенты, которые будут доступны в последующих задачах (task).
    Используется, если порядок выполнения задач внутри таск-сета не имеет значения.
    """

    users_gateway_client: UsersGatewayHTTPClient
    cards_gateway_client: CardsGatewayHTTPClient
    operations_gateway_client: OperationsGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    documents_gateway_client: DocumentsGatewayHTTPClient

    def on_start(self) -> None:
        """
        Метод вызывается перед запуском задач TaskSet.
        Здесь создаются API клиенты с использованием контекста окружения Locust.
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_http_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_http_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_http_client(self.user.environment)





class GatewayHTTPSequentialTaskSet(SequentialTaskSet):
    """
    Базовый SequentialTaskSet для HTTP-сценариев, где важен порядок выполнения задач.

    Задачи внутри такого таск-сета будут выполняться строго по очереди — сверху вниз.
    Также здесь инициализируются те же API клиенты, что и в обычном TaskSet.
    """
    users_gateway_client: UsersGatewayHTTPClient
    cards_gateway_client: CardsGatewayHTTPClient
    operations_gateway_client: OperationsGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    documents_gateway_client: DocumentsGatewayHTTPClient

    def on_start(self) -> None:
        """
        Создание API клиентов для последовательного сценария.
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_http_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_http_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_http_client(self.user.environment)



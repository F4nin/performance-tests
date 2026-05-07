from clients.http.client import HttpClient, Response
from clients.http.gateway.cards.cards_schema import IssueVirtualCardRequestSchema, IssuePhysicalCardRequestSchema
from tools.routes import APIRoutes


class CardsGatewayHTTPClient(HttpClient):
    """
    Клиент для работы с /api/v1/cards
    """
    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """
        Публичный метод для создания пользователя
        :param request: словарь со структурой IssueVirtualCardRequestSchema
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.CARDS, json=request.model_dump(by_alias=True))

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """
        Публичный метод для создания пользователя
        :param request: словарь со структурой IssuePhysicalCardRequestSchema
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.CARDS, json=request.model_dump(by_alias=True))



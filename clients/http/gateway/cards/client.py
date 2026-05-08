from clients.http.gateway.client import HttpClient, Response
from clients.http.gateway.cards.cards_schema import IssueVirtualCardRequestSchema, IssuePhysicalCardRequestSchema
from tools.routes import APIRoutes


class CardsGatewayHTTPClient(HttpClient):
    """
    Клиент для работы с /api/v1/cards
    """
    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """
        Выпуск виртуальной карты.

        :param request: Словарь с данными для выпуска виртуальной карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(f"{APIRoutes.CARDS}/issue-virtual-card", json=request.model_dump(by_alias=True))

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """
        Выпуск физической карты.

        :param request: Словарь с данными для выпуска физической карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(f"{APIRoutes.CARDS}/issue-physical-card", json=request.model_dump(by_alias=True))



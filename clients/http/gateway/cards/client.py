from clients.http.client import HttpClient, Response
from clients.http.gateway.cards.cards_schema import IssueVirtualCardRequestSchema, IssuePhysicalCardRequestSchema, \
    IssueVirtualCardResponseSchema, IssuePhysicalCardResponseSchema
from clients.http.gateway.client import build_gateway_http_client
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

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseSchema:
        request = IssueVirtualCardRequestSchema(userId=user_id, accountId=account_id)
        response = self.issue_virtual_card_api(request)
        return IssueVirtualCardResponseSchema.model_validate_json(response.text)

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseSchema:
        request = IssuePhysicalCardRequestSchema(userId=user_id, accountId=account_id)
        response = self.issue_physical_card_api(request)
        return IssuePhysicalCardResponseSchema.model_validate_json(response.text)

def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())

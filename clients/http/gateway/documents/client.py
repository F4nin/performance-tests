from clients.http.client import HttpClient, Response
from tools.routes import APIRoutes


class DocumentsGatewayHTTPClient(HttpClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """
    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифа по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"{APIRoutes.DOCUMENTS}/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контракта по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"{APIRoutes.DOCUMENTS}/contract-document/{account_id}")
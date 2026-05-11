from clients.http.client import HttpClient, Response, HttpClientExtensions
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.documents.documents_schema import GetTariffDocumentResponseSchema, \
    GetContractDocumentResponseSchema
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
        return self.get(
            f"{APIRoutes.DOCUMENTS}/tariff-document/{account_id}",
            extensions=HttpClientExtensions(route=f"{APIRoutes.DOCUMENTS}/tariff-document/{{account_id}}"))

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контракта по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(
            f"{APIRoutes.DOCUMENTS}/contract-document/{account_id}",
            extensions=HttpClientExtensions(route=f"{APIRoutes.DOCUMENTS}/contract-document/{{account_id}}"))

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
from httpx import Response

from clients.http.client import HttpClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.users.users_schema import CreateUserRequestSchema
from tools.routes import APIRoutes


class UsersGatewayHTTPClient(HttpClient):
    """
    Клиент для работы с /api/v1/users
    """

    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получения пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.client.get(f"{APIRoutes.USERS}/{user_id}")

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        :param request: словарь со структурой CreateUserRequestSchema
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.USERS, json=request.model_dump(by_alias=True))

def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())

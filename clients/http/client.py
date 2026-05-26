from typing import Any, TypedDict

from httpx import Client, URL, Response, QueryParams

class HttpClientExtensions(TypedDict, total=False):
    route: str

class HttpClient:
    def __init__(self, client: Client):
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None, extensions: HttpClientExtensions | None = None) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :param extensions: Дополнительные параметры передаваемые через HTTPX extentions.
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url, params=params, extensions=extensions)

    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            extensions: HttpClientExtensions | None = None,
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param extensions: Дополнительные параметры передаваемые через HTTPX extentions.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url, json=json, extensions=extensions)


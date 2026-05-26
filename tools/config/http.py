from pydantic import BaseModel, HttpUrl

class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float = 100.0

    @property
    def client_url(self):
        """
        Возвращает URL в виде строки, пригодной для передачи в httpx.Client.

        Почему это важно:
        - Pydantic хранит url как объект HttpUrl.
        - httpx.Client требует base_url именно как строку.
        - Если передать HttpUrl напрямую, будет ошибка типов.
        """
        return str(self.url)
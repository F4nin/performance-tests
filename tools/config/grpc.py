from pydantic import BaseModel, HttpUrl

class GRPCClientConfig(BaseModel):
    host: str = "localhost"
    port: int = 9003

    @property
    def client_url(self):
        """
        Возвращает адрес подключения в формате host:port,
        который требуется для создания gRPC-канала через insecure_channel().
        """
        return f"{self.host}:{self.port}"

from pydantic import BaseModel, Field

from clients.http.gateway.cards.cards_schema import CardSchema


class AccountViewSchema(BaseModel):
    """
     Описание структуры аккаунта.
     """
    id: str
    type: str
    cards: list[CardSchema]
    status: str
    balance: int


class GetAccountsQuerySchema(BaseModel):
    """
    Структура данных для получения списка счетов пользователя.
    """
    user_id: str = Field(alias="userId")

class OpenDepositAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия депозитного счета.
    """
    user_id: str = Field(alias="userId")

class OpenSavingsAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия сберегательного счета.
    """
    user_id: str = Field(alias="userId")

class OpenDebitCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия дебетового счета.
    """
    user_id: str = Field(alias="userId")

class OpenCreditCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия кредитного счета.
    """
    user_id: str = Field(alias="userId")

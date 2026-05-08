from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict

from clients.http.gateway.cards.cards_schema import CardSchema


class AccountType(StrEnum):
    DEPOSIT = "DEPOSIT"
    SAVINGS = "SAVINGS"
    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"


class AccountStatus(StrEnum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PENDING_CLOSURE = "PENDING_CLOSURE"


class AccountViewSchema(BaseModel):
    """
     Описание структуры аккаунта.
     """
    id: str
    type: str
    cards: list[CardSchema]
    status: AccountStatus
    balance: float


class GetAccountsQuerySchema(BaseModel):
    """
    Структура данных для получения списка счетов пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

class OpenDepositAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия депозитного счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

class OpenSavingsAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия сберегательного счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

class OpenDebitCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия дебетового счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

class OpenCreditCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия кредитного счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

class GetAccountsResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка счетов.
    """
    accounts: list[AccountViewSchema]

class OpenDepositAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия депозитного счета.
    """
    account: AccountViewSchema

class OpenSavingsAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия сберегательного счета.
    """
    account: AccountViewSchema

class OpenDebitCardAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия дебетового счета.
    """
    account: AccountViewSchema

class OpenCreditCardAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия кредитного счета.
    """
    account: AccountViewSchema



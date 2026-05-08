from pydantic import BaseModel, Field

from clients.http.gateway.cards.cards_schema import CardSchema


class AccountViewSchema(BaseModel):
    id: str
    type: str
    cards: list[CardSchema]
    status: str
    balance: int


class GetAccountsQuerySchema(BaseModel):
    user_id: str = Field(alias="userId")

class OpenDepositAccountRequestSchema(BaseModel):
    user_id: str = Field(alias="userId")

class OpenSavingsAccountRequestSchema(BaseModel):
    user_id: str = Field(alias="userId")

class OpenDebitCardAccountRequestSchema(BaseModel):
    user_id: str = Field(alias="userId")

class OpenCreditCardAccountRequestSchema(BaseModel):
    user_id: str = Field(alias="userId")

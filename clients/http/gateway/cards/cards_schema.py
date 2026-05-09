from pydantic import BaseModel, Field, EmailStr, ConfigDict
from tools.fakers import fake
from datetime import date
from enum import StrEnum

class CardType(StrEnum):
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(StrEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class CardPaymentSystem(StrEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"

class CardSchema(BaseModel):
    """
     Описание структуры карты.
     """
    id: str
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: str = Field(alias="accountId")
    card_number: str = Field(alias="cardNumber")
    card_holder: str = Field(alias="cardHolder")
    expiry_date: date = Field(alias="expiryDate")
    payment_system: CardPaymentSystem = Field(alias="paymentSystem")

class IssueVirtualCardRequestSchema(BaseModel):
    """
    Описание структуры запроса для создания виртуальной
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")
    account_id: str = Field(alias="accountId")

class IssuePhysicalCardRequestSchema(BaseModel):
    """
    Описание структуры запроса для создания физической карты
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")
    account_id: str = Field(alias="accountId")

class IssueVirtualCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска виртуальной карты.
    """
    card: CardSchema

class IssuePhysicalCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска физической карты.
    """
    card: CardSchema

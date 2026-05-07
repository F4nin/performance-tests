from pydantic import BaseModel, Field, EmailStr, ConfigDict
from tools.fakers import fake

class CardSchema(BaseModel):
    """
     Описание структуры карты.
     """
    id: str
    pin: str
    cvv: str
    type: str
    status: str
    account_id: str = Field(alias="accountId")
    card_number: str = Field(alias="cardNumber")
    card_holder: str = Field(alias="cardHolder")
    expiry_date: str = Field(alias="expiryDate")
    payment_system: str = Field(alias="paymentSystem")

class IssueVirtualCardRequestSchema(BaseModel):
    """
    Описание структуры запроса для создания виртуальной
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId", default=fake.uuid4)
    account_id: str = Field(alias="accountId", default=fake.uuid4)

class IssuePhysicalCardRequestSchema(BaseModel):
    """
    Описание структуры запроса для создания физической карты
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId", default=fake.uuid4)
    account_id: str = Field(alias="accountId", default=fake.uuid4)

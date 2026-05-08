from pydantic import BaseModel, Field

class MakeOperationRequestSchema(BaseModel):
    """
    Базовая структура тела запроса для создания финансовой операции.
    """
    status: str
    amount: float
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")

class GetOperationsQuerySchema(BaseModel):
    """
    Структура query параметров запроса для получения списка операций по счёту.
    """
    account_id: str = Field(alias="accountId")

class GetOperationsSummaryQuerySchema(BaseModel):
    """
    Структура query параметров запроса для получения статистики по операциям счёта.
    """
    account_id: str = Field(alias="accountId")

class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции комиссии.
    """
    pass

class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции пополнения.
    """
    pass

class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции кэшбэка.
    """
    pass

class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции перевода.
    """
    pass

class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции покупки.

    Дополнительное поле:
    - category: категория покупки.
    """
    category: str

class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции оплаты по счёту.
    """
    pass

class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции снятия наличных.
    """
    pass
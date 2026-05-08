
from httpx import Response, QueryParams

from clients.http.gateway.client import HttpClient
from clients.http.gateway.operations.operations_schema import GetOperationsQuerySchema, GetOperationsSummaryQuerySchema, \
    MakeFeeOperationRequestSchema, MakeTopUpOperationRequestSchema, MakeCashbackOperationRequestSchema, \
    MakeTransferOperationRequestSchema, MakePurchaseOperationRequestSchema, MakeBillPaymentOperationRequestSchema, \
    MakeCashWithdrawalOperationRequestSchema
from tools.routes import APIRoutes


class OperationsGatewayHTTPClient(HttpClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Получает информацию об операции по её идентификатору.

        :param operation_id: Уникальный идентификатор операции.
        :return: Объект httpx.Response с данными об операции.
        """
        return self.get(f"{APIRoutes.OPERATIONS}/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Получает чек по заданной операции.

        :param operation_id: Уникальный идентификатор операции.
        :return: Объект httpx.Response с чеком по операции.
        """
        return self.get(f"{APIRoutes.OPERATIONS}/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        """
        Получает список операций по счёту.

        :param query: Словарь с параметром accountId.
        :return: Объект httpx.Response с операциями по счёту.
        """
        return self.get(f"{APIRoutes.OPERATIONS}", params=QueryParams(**query))

    def get_operations_summary_api(self, query: GetOperationsSummaryQuerySchema) -> Response:
        """
        Получает сводную статистику операций по счёту.

        :param query: Словарь с параметром accountId.
        :return: Объект httpx.Response с агрегированной информацией.
        """
        return self.get(f"{APIRoutes.OPERATIONS}/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeFeeOperationRequestSchema) -> Response:
        """
        Создаёт операцию комиссии.

        :param request: Тело запроса с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-fee-operation", json=request.model_dump(by_alias=True))

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestSchema) -> Response:
        """
        Создаёт операцию пополнения счёта.

        :param request: Тело запроса с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-top-up-operation", json=request.model_dump(by_alias=True))

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestSchema)-> Response:
        """
        Создаёт операцию начисления кэшбэка.

        :param request: Тело запроса с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-cashback-operation", json=request.model_dump(by_alias=True))

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestSchema) -> Response:
        """
        Создаёт операцию перевода средств.

        :param request: Тело запроса с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-transfer-operation", json=request.model_dump(by_alias=True))

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        """
        Создаёт операцию покупки.

        :param request: Тело запроса с параметрами операции, включая категорию.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-purchase-operation", json=request.model_dump(by_alias=True))

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestSchema) -> Response:
        """
        Создаёт операцию оплаты счёта.

        :param request: Тело запроса с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-bill-payment-operation", json=request.model_dump(by_alias=True))

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestSchema) -> Response:
        """
        Создаёт операцию снятия наличных средств.

        :param request: Тело запроса с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(f"{APIRoutes.OPERATIONS}/make-cash-withdrawal-operation", json=request.model_dump(by_alias=True))








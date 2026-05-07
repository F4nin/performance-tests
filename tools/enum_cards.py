from enum import Enum

class CardType(str, Enum):
    """
    Тип банковской карты
    """
    UNSPECIFIED = "UNSPECIFIED"
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(str, Enum):
    """
    Тип статуса банковской карты
    """
    UNSPECIFIED = "UNSPECIFIED"
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"

class CardPaymentSystem(str, Enum):
    """
    Тип платежной системы банковской карты
    """
    UNSPECIFIED = "UNSPECIFIED"
    MASTERCARD = "MASTERCARD"
    VISA = "VISA"




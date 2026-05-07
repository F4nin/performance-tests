from enum import Enum

class APIRoutes(str, Enum):
    USERS = "api/v1/users"
    CARDS = "api/v1/cards"
    ACCOUNTS = "api/v1/accounts"
    DOCUMENTS = "api/v1/documents"
    OPERATIONS = "api/v1/operations"

    def __str__(self):
        return self.value


from enum import Enum
from typing import Literal


class ActionTypeEnum(str, Enum):
    USER_CREATED = "user_created"
    USER_MODIFIED = "user_modified"
    USER_DELETED = "user_deleted"
    USER_LOGGED_IN = "user_logged_in"


ActionType = Literal[
    "user_created", "user_modified", "user_deleted", "user_logged_in"
]

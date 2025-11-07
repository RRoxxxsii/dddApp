from src.application.dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    first_name: str
    last_name: str

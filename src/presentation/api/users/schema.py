from src.presentation.api.request import BaseRequest


class CreateUser(BaseRequest):
    first_name: str
    last_name: str
    password: str
    email: str

from src.application.usecases.users.dto import UserDTO
from src.domain.users.entities import User


class UserMapper:
    @staticmethod
    def map_user(user: User):
        return UserDTO(
            id=user.id.value,
            first_name=user.first_name,
            last_name=user.last_name,
        )

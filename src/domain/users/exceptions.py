from src.domain.exceptions import ValidationException


class PasswordException(ValidationException):
    pass


class PasswordTooShortException(PasswordException):
    def __init__(self, min_length: int, actual_length: int):
        self.min_length = min_length
        self.actual_length = actual_length
        self._message = (
            f"Password must be at least {min_length} characters long, "
            f"got {actual_length}"
        )
        super().__init__(self._message)


class PasswordTooLongException(PasswordException):
    def __init__(self, max_length: int, actual_length: int):
        self.max_length = max_length
        self.actual_length = actual_length
        self._message = (
            f"Password must be no more than {max_length} characters long, "
            f"got {actual_length}"
        )
        super().__init__(self._message)

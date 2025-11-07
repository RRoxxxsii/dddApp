class DomainException(Exception):
    def __init__(self, message: str = ""):
        self._message = message
        super().__init__(message)

    @property
    def message(self) -> str:
        return self._message or str(self)


class ValidationException(DomainException):
    """Некорректные данные (непрошедшие валидацию)."""

    pass


class NotFoundException(DomainException):
    """Сущность не найдена (агрегат, объект, коллекция)."""

    pass


class AlreadyExistsException(DomainException):
    """Попытка создать дубликат (уникальное поле уже занято)."""

    pass


class UnauthorizedException(DomainException):
    """Доступ запрещен (нет прав на операцию)."""

    pass


class InvalidOperationException(DomainException):
    """Недопустимая бизнес-операция (нарушение инвариантов)."""

    pass

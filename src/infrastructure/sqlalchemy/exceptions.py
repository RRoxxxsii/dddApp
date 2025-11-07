class RepositoryException(Exception):
    """Базовое исключение для всех ошибок репозитория"""


class RepositoryNotFoundException(RepositoryException):
    """Сущность не найдена"""


class RepositoryAlreadyExistsException(RepositoryException):
    """Сущность уже существует"""


class RepositoryConstraintViolationException(RepositoryException):
    """Нарушение ограничений базы данных"""

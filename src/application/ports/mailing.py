from abc import ABC, abstractmethod


class ABCNotificationClient(ABC):
    @abstractmethod
    async def send_message(self, subject: str, body: str, email: str) -> None:
        raise NotImplementedError

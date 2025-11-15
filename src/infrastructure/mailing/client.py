from src.application.ports.mailing import ABCNotificationClient


class ConsoleMailingClient(ABCNotificationClient):
    async def send_message(self, subject: str, body: str, email: str) -> None:
        print(f"Message with {subject} {body} sent to {email}")

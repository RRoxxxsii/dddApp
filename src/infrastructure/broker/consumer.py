import asyncio
import json
import traceback
from abc import abstractmethod, ABC
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer

from src.infrastructure.broker.handlers import ABCHandler


class MessageConsumer(ABC):

    @abstractmethod
    async def consume(self, topic_handlers: dict[str, ABCHandler]) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass


@dataclass
class KafkaConfig:
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = 'earliest'
    enable_auto_commit: bool = False
    session_timeout_ms: int = 6000
    max_poll_interval_ms: int = 300000


class KafkaMessageConsumer(MessageConsumer):
    def __init__(self, config: KafkaConfig):
        self.config = config
        self.consumer: AIOKafkaConsumer | None = None
        self._running = False

    async def consume(self, topic_handlers: dict[str, ABCHandler]) -> None:

        self.consumer = AIOKafkaConsumer(
            *topic_handlers.keys(),
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=self.config.group_id,
            auto_offset_reset=self.config.auto_offset_reset,
            enable_auto_commit=self.config.enable_auto_commit,
            session_timeout_ms=self.config.session_timeout_ms,
            max_poll_interval_ms=self.config.max_poll_interval_ms
        )

        await self.consumer.start()
        self._running = True

        try:
            async for message in self.consumer:
                try:
                    handler: ABCHandler = topic_handlers[message.topic]
                    data = json.loads(message.value.decode('utf-8'))
                    if asyncio.iscoroutinefunction(handler.handle):
                        await handler.handle(data)
                    else:
                        handler.handle(data)  # type: ignore

                except json.JSONDecodeError as e:
                    traceback.print_exc()
                except KeyError as e:
                    traceback.print_exc()
                except Exception as e:
                    traceback.print_exc()

        finally:
            await self.stop()

    async def stop(self) -> None:
        if self.consumer:
            await self.consumer.stop()

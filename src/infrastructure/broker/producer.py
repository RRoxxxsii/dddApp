import json
from abc import ABC, abstractmethod
from typing import Any

from aiokafka import AIOKafkaProducer as _AIOKafkaProducer


class ABCProducer(ABC):
    @abstractmethod
    async def send(
        self,
        topic: str,
        value: Any = None,
        key: Any = None,
        partition: Any = None,
        timestamp_ms: Any = None,
        headers: Any = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError


class AIOKafkaProducer(ABCProducer):
    def __init__(self, bootstrap_servers: str, **kwargs):
        self._kafka = _AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers, **kwargs
        )

    async def send(
        self,
        topic: str,
        value: Any = None,
        key: Any = None,
        partition: Any = None,
        timestamp_ms: Any = None,
        headers: Any = None,
    ) -> None:
        if key:
            key = key.encode("utf-8")

        if value:
            value = json.dumps(value).encode("utf-8")

        await self._kafka.send(
            topic, value, key, partition, timestamp_ms, headers
        )

    async def start(self) -> None:
        await self._kafka.start()

    async def stop(self) -> None:
        await self._kafka.stop()

import asyncio
import logging
import traceback
from datetime import datetime
from typing import Any

from sqlalchemy import select

from src.domain.analytics.entity import ActionTypeEnum
from src.infrastructure.broker.producer import ABCProducer
from src.infrastructure.sqlalchemy.model import OutboxMessageORM

logger = logging.getLogger(__name__)


class OutboxProcessor:
    def __init__(self, db_provider: Any, producer: ABCProducer):
        self._db_provider = db_provider
        self._producer = producer

    async def process_outbox_messages(self):
        async for session in self._db_provider():
            try:
                stmt = (
                    select(OutboxMessageORM)
                    .where(OutboxMessageORM.is_processed.is_(False))
                    .limit(100)
                )

                result = await session.execute(stmt)
                messages = result.scalars().all()

                for message in messages:
                    message: OutboxMessageORM
                    try:
                        if (
                            message.event_type
                            == ActionTypeEnum.ORDER_CREATED.value
                        ):
                            await self._producer.send(
                                value=message.payload,
                                topic="order.created",
                                key=f"orders_{message.aggregate_id}",
                            )

                        message.is_processed = True
                        message.processed_at = datetime.now()
                        await session.commit()

                        logger.info(f"Processed outbox message {message.id}")

                    except Exception as e:
                        traceback.print_exc()
                        logger.error(
                            f"Failed to process outbox message "
                            f"{message.id}: {e}"
                        )
                        await session.rollback()

            except Exception as e:
                logger.error(f"Error in outbox processing: {e}")

    async def start_processing(self):
        while True:
            try:
                await self.process_outbox_messages()
            except Exception as e:
                logger.error(f"Error in outbox processing loop: {e}")

            await asyncio.sleep(5)

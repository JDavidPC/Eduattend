# src/attendance_service/infrastructure/adapters/outbound/rabbitmq_event_publisher.py
import json
import logging
import os
from dataclasses import asdict
from datetime import UTC, datetime

import pika

from ....domain.model.absence_event import AbsenceEvent
from ....domain.service.absence_event_service import IAbsenceEventPublisher

LOGGER = logging.getLogger(__name__)


class RabbitMQEventPublisher(IAbsenceEventPublisher):
    def __init__(self, rabbitmq_url: str | None = None) -> None:
        self._rabbitmq_url = rabbitmq_url or os.getenv(
            "RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/"
        )

    def publish_absence_limit_reached(
        self,
        student_id: str,
        student_email: str,
        course_id: str,
        absence_count: int,
    ) -> None:
        event = AbsenceEvent(
            event="ABSENCE_LIMIT_REACHED",
            student_id=student_id,
            student_email=student_email,
            course_id=course_id,
            count=absence_count,
            timestamp=datetime.now(UTC).isoformat(),
        )

        payload = json.dumps(asdict(event), ensure_ascii=True)

        connection = None
        try:
            parameters = pika.URLParameters(self._rabbitmq_url)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.exchange_declare(
                exchange="absence_events",
                exchange_type="direct",
                durable=True,
            )
            channel.basic_publish(
                exchange="absence_events",
                routing_key="absence_limit",
                body=payload,
                properties=pika.BasicProperties(content_type="application/json"),
            )
        except Exception as exc:
            LOGGER.error("No se pudo publicar evento en RabbitMQ: %s", exc)
        finally:
            if connection is not None and connection.is_open:
                connection.close()

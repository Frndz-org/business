import os

from contextlib import asynccontextmanager
from django.conf import settings
from faststream.kafka import KafkaBroker
from faststream.redis import RedisBroker

if 'RENDER' not in os.environ:
    broker = KafkaBroker(settings.KAFKA_SERVERS)
else:
    REDIS_SERVER = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    broker = RedisBroker(REDIS_SERVER)


@broker.subscriber('new-notification')
async def handle_notification(message):
    print(message)


@asynccontextmanager
async def broker_lifespan(app):
    await broker.start()
    try:
        yield
    finally:
        await broker.close()

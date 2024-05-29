"""
ASGI config for business project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business.settings')

from business.faststream import broker_lifespan

application = Starlette(
    routes=(
        Mount("/static", StaticFiles(directory="static"), name="static"),
        Mount("/", get_asgi_application()),
    ),
    lifespan=broker_lifespan
)

application = get_asgi_application()

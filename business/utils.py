import asyncio
import random
import re
import string
import time
from datetime import datetime, timedelta
from typing import Optional, Any

import jwt
from django.conf import settings
from django.http import HttpRequest
from ninja.errors import HttpError
from ninja.security import HttpBearer


def broker_publish(topic: str, payload: dict):
    """
    A wrapper to publish stream data synchronously through
    FastStream
    """

    async def abroker_publish():
        from business.faststream import broker
        await broker.start()
        try:
            print(topic, payload)
            await broker.publisher(topic).publish(payload)
        finally:
            await broker.close()

    asyncio.get_event_loop().run_until_complete(abroker_publish())


class TokenBasedAuthorization(HttpBearer):
    """
    Responsible for handling JWT authentication
    """

    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        """
        Authenticates a given token
        """

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

            return payload["user"]

        except (jwt.exceptions.ExpiredSignatureError, jwt.DecodeError):
            print("Token is expired")
            raise HttpError(401, "Token expired")

    @staticmethod
    def validate_refresh_token(token):
        try:
            payload = jwt.decode(token, settings.JWT_REFRESH_KEY, algorithms=["HS256"])
            print(payload)
            if time.time() >= float(payload['exp']):
                return False
            return payload
        except (jwt.exceptions.ExpiredSignatureError, jwt.DecodeError):
            return False

    @staticmethod
    def generate_access_token(user):
        access_token_payload = {
            'token_type': 'access',
            'user': {
                'id': user.identity.identifier.__str__(),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'verified': user.identity.verified,
                'permissions': [permission.split('.')[1] for permission in user.get_all_permissions()]
            },
            'exp': datetime.utcnow() + timedelta(minutes=float(settings.JWT_ACCESS_TOKEN_LIFETIME)),
            'iat': datetime.utcnow(),
        }
        access_token = TokenBasedAuthorization._create_token(claim=access_token_payload,
                                                             secret_key=settings.JWT_SECRET_KEY, algorithm='HS256')
        return access_token

    @staticmethod
    def generate_refresh_token(user):
        refresh_token_payload = {
            'token_type': 'refresh',
            'user_id': user.identity.identifier.__str__(),
            'exp': datetime.utcnow() + timedelta(minutes=float(settings.JWT_REFRESH_TOKEN_LIFETIME)),
            'iat': datetime.utcnow()
        }
        refresh_token = TokenBasedAuthorization._create_token(claim=refresh_token_payload,
                                                              secret_key=settings.JWT_REFRESH_KEY, algorithm='HS256')

        return refresh_token

    @staticmethod
    def _create_token(claim, secret_key: str, algorithm='HS256'):
        return jwt.encode(claim, secret_key, algorithm=algorithm)


class Utility:

    @staticmethod
    def get_random_string(length=10, chars=string.ascii_lowercase + string.digits):
        """
        Returns a minimum of 10 random string of characters
        :param length:
        :param chars:
        :return:
        """
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def remove_html_tags(text):
        """
        Removes all html tags from a given text
        :param text:
        :return:
        """
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    @staticmethod
    def placeholder_replace(payload: dict, text):
        """
        Replaces payload keys with payload values in a given text
        :param payload:
        :param text:
        :return string:
        """
        rep = dict((re.escape(k), v) for k, v in payload.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

        return text

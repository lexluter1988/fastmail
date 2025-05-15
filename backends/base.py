from __future__ import annotations

import os
import typing
from typing import Type

from backends.registry import registry
from backends.ses import AwsSesEmailBackend
from backends.unisender_go import UnisenderGoEmailBackend

if typing.TYPE_CHECKING:
    from base.message import EmailMessage, EmailServiceProtocol


class BaseEmailBackend:
    _default_service = None

    @classmethod
    def register(cls, name: str, service_class: Type) -> None:
        registry[name] = service_class

    @classmethod
    def configure(cls) -> None:
        service_type = os.getenv('EMAIL_SERVICE_TYPE')
        if not service_type:
            raise ValueError('Environment variable EMAIL_SERVICE_TYPE is not set')

        if service_type not in registry:
            raise ValueError(
                f"Unknown service type: {service_type}. "
                f"Available types: {', '.join(registry.keys())}"
            )

        if service_type == 'ses':
            _default_service = AwsSesEmailBackend(
                endpoint_url=os.getenv('AWS_ENDPOINT_URL'),
                region_name=os.getenv('AWS_REGION_NAME'),
                access_key=os.getenv('AWS_ACCESS_KEY_ID'),
                secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            )
        elif service_type == 'unisender_go':
            _default_service = UnisenderGoEmailBackend(
                api_key=os.getenv('UNISENDER_GO_API_KEY'),
            )
        else:
            raise ValueError(f"Unsupported service type in environment: {service_type}")
        cls._default_service = _default_service

    @classmethod
    def get_default(cls) -> EmailServiceProtocol:
        if cls._default_service is None:
            print('here')
            try:
                cls.configure()
            except Exception as e:
                raise RuntimeError(f"Default email service not configured: {str(e)}")

        return cls._default_service

    @classmethod
    def has_default(cls) -> bool:
        if cls._default_service is not None:
            return True
        try:
            cls.configure()
            return True
        except ValueError:
            return False

    @classmethod
    def send(cls, message: EmailMessage) -> str:
        return cls.get_default().send_message(message)

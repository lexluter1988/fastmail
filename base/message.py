from __future__ import annotations

from abc import abstractmethod
from typing import List, Protocol

from backends.base import BaseEmailBackend


class EmailServiceProtocol(Protocol):
    @abstractmethod
    def send_message(self, message: EmailMessage) -> str:
        ...


class EmailMessage:
    def __init__(
        self,
        from_email: str,
        to: List[str],
        subject: str,
        body: str,
    ):
        self.from_email = from_email
        self.to = to
        self.subject = subject
        self.body = body

    def send(self) -> str:
        if not BaseEmailBackend.has_default():
            raise RuntimeError(
                'Default email service not configured. '
                'Use EmailService.configure() or set EMAIL_SERVICE_TYPE environment variable.'
            )

        return BaseEmailBackend.get_default().send_message(self)

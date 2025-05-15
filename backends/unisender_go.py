from __future__ import annotations

import os
import typing

import requests

BASE_URL = 'https://go1.unisender.ru/ru/transactional/api/v1'

if typing.TYPE_CHECKING:
    from backends.base import EmailMessage


class UnisenderGoEmailBackend:
    def __init__(
        self,
        api_key: str,
    ):
        self.api_key = api_key or os.getenv('UNISENDER_GO_API_KEY')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': api_key,
        }

    def send_message(self, message: EmailMessage) -> str:
        try:
            request_body = {
                'message': {
                    'recipients': [{'email': email} for email in message.to],
                    'body': {
                        'plaintext': message.body,
                    },
                    'subject': message.subject,
                    'from_email': message.from_email,
                }
            }

            with requests.Session() as session:
                r = session.post(
                    BASE_URL + '/email/send.json', json=request_body, headers=self.headers
                )
                r.raise_for_status()
                return r.json()
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise Exception(f"Email sending failed: {str(e)}")

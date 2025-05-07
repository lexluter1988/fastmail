from __future__ import annotations

import os
import typing
from typing import Optional

import boto3
from botocore.exceptions import ClientError

if typing.TYPE_CHECKING:
    from backends.base import EmailMessage


class AwsSesEmailBackend:
    def __init__(
        self,
        region_name: str,
        access_key: str,
        secret_key: str,
        endpoint_url: Optional[str] = None,
    ):
        self.ses = boto3.client(
            'sesv2',
            endpoint_url=endpoint_url or os.getenv('AWS_ENDPOINT_URL'),
            region_name=region_name or os.getenv('AWS_REGION_NAME'),
            aws_access_key_id=access_key or os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=secret_key or os.getenv('AWS_SECRET_ACCESS_KEY'),
        )

    def send_message(self, message: EmailMessage) -> str:
        try:
            body = {'Text': {'Data': message.body}}
            subject = {'Data': message.subject}
            response = self.ses.send_email(
                FromEmailAddress=message.from_email,
                Destination={'ToAddresses': message.to},
                Content={'Simple': {'Subject': subject, 'Body': body}},
            )
            return response['MessageId']
        except ClientError as e:
            raise Exception(f"Email sending failed: {str(e)}")

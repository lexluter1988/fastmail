# fastmail

Minimalistic email client supporting AWS SES compatible clients and others.

## Author

Author: lexxsmith@gmail.com

## Version

0.1.0

## License

License: MIT

## AWS Example

Export environment variables

```
export EMAIL_SERVICE_TYPE=ses
export AWS_ENDPOINT_URL=https://localhost
export AWS_REGION_NAME=central1
export AWS_ACCESS_KEY_ID=<key_id>
export AWS_SECRET_ACCESS_KEY=<secret>
```

Send message from REPL

```python
from base.message import EmailMessage

try:
    message = EmailMessage(
        from_email='sender@example.com',
        to=['recipient@example.com'],
        subject='Test Subject',
        body='Test Body',
    )
    message_id = message.send()
    print(f"Message send. ID: {message_id}")

except Exception as e:
    raise
```


## Unisender Go Example

Export environment variables

```
export EMAIL_SERVICE_TYPE=unisender_go
export UNISENDER_GO_API_KEY=<secret>
```

Send message from REPL

```python
from base.message import EmailMessage

try:
    message = EmailMessage(
        from_email='sender@example.com',
        to=['recipient@example.com'],
        subject='Test Subject',
        body='Test Body',
    )
    message_id = message.send()
    print(f"Message send. ID: {message_id}")

except Exception as e:
    raise
```

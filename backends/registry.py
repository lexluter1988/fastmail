from backends.ses import AwsSesEmailBackend

registry = {
    'ses': AwsSesEmailBackend,
}

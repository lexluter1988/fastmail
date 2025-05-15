from backends.ses import AwsSesEmailBackend
from backends.unisender_go import UnisenderGoEmailBackend

registry = {'ses': AwsSesEmailBackend, 'unisender_go': UnisenderGoEmailBackend}

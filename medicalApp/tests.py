from django.test import TestCase



import mock
from django.core.files import File

file_mock = mock.MagicMock(spec=File, name='FileMock')

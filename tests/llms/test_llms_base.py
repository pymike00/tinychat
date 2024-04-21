import unittest
from unittest.mock import patch

from tinychat.llms.base import BaseLLMClient
from tinychat.settings import SECRETS_FILE_PATH


class TestBaseLLMClient(unittest.TestCase):

    @patch('tinychat.llms.base.get_secret')
    def test_api_key_setter_valid_key(self, mock_get_secret):
        mock_get_secret.return_value = 'test_api_key'
        client = BaseLLMClient(api_key_name='test_api_key_name')
        self.assertEqual(client.api_key, 'test_api_key')

    @patch('tinychat.llms.base.get_secret')
    def test_api_key_setter_invalid_key(self, mock_get_secret):
        mock_get_secret.return_value = None
        with self.assertRaises(ValueError) as context:
            BaseLLMClient(api_key_name='invalid_api_key_name')
        self.assertIn('invalid_api_key_name was not found in', str(context.exception))
        self.assertIn(SECRETS_FILE_PATH, str(context.exception))

    @patch('tinychat.llms.base.get_secret')
    def test_default_headers(self, mock_get_secret):
        mock_get_secret.return_value = 'some-api-key'
        client = BaseLLMClient(api_key_name='test_api_key_name')
        expected_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer some-api-key",
        }
        self.assertEqual(client.default_headers(), expected_headers)


import unittest
from unittest.mock import patch, Mock

from requests.models import Response

from tinychat.llms.mistral import MistralClient


class TestMistralClient(unittest.TestCase):

    @patch('tinychat.llms.openai.requests.post')
    def test_perform_chat_request_success(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "test response"}}
            ]
        }
        mock_post.return_value = mock_response

        client = MistralClient(model_name='test_model')
        messages = [{"role": "user", "content": "hello"}]
        response = client.perform_chat_request(messages)
        self.assertEqual(response, "test response")

    @patch('tinychat.llms.openai.requests.post')
    def test_perform_chat_request_failure(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        client = MistralClient(model_name='test_model')
        messages = [{"role": "user", "content": "hello"}]
        with self.assertRaises(ValueError) as context:
            client.perform_chat_request(messages)
        self.assertIn('Server responded with an error. Status Code: 400', str(context.exception))

    @patch('tinychat.llms.openai.requests.post')
    def test_perform_chat_request_invalid_response_format(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        client = MistralClient(model_name='test_model')
        messages = [{"role": "user", "content": "hello"}]
        with self.assertRaises(KeyError) as context:
            client.perform_chat_request(messages)
        self.assertIn('Invalid response format received from server.', str(context.exception))


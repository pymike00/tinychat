import unittest
from unittest.mock import patch, Mock

from requests.models import Response

from tinychat.llms.google import GoogleAIClient


class TestGoogleAIClient(unittest.TestCase):
    @patch("tinychat.llms.google.requests.post")
    def test_perform_chat_request_success(self, mock_post):
        expected_response = "test response text"
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": expected_response}]}}]
        }
        mock_post.return_value = mock_response

        client = GoogleAIClient()
        messages = [{"role": "user", "content": "hello"}]
        response = client.perform_chat_request(messages)
        self.assertEqual(response, expected_response)

    @patch("tinychat.llms.google.requests.post")
    def test_perform_chat_request_failure(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        client = GoogleAIClient()
        messages = [{"role": "user", "content": "hello"}]
        with self.assertRaises(ValueError) as context:
            client.perform_chat_request(messages)
        self.assertIn(
            "Server responded with an error. Status Code: 400", str(context.exception)
        )

    @patch("tinychat.llms.google.requests.post")
    def test_perform_chat_request_invalid_response_format(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"unexpected": "invalid-response-format"}
        mock_post.return_value = mock_response

        client = GoogleAIClient()
        messages = [{"role": "user", "content": "hello"}]
        with self.assertRaises(KeyError) as context:
            client.perform_chat_request(messages)
        self.assertIn(
            "Invalid response format received from server.", str(context.exception)
        )

import unittest
from unittest.mock import patch, Mock

import requests

from tinychat.llms.cohere import CohereClient


class TestCohereClientStreaming(unittest.TestCase):
    @patch("tinychat.llms.cohere.requests.post")
    def test_perform_stream_request_success(self, mock_post):
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        client = CohereClient()
        chat_history = [
            {"role": "User", "message": "hello"},
            {"role": "Chatbot", "message": "hello!"},
        ]
        response = client.perform_stream_request("how are you?", chat_history)
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200)

    @patch("tinychat.llms.cohere.requests.post")
    def test_perform_stream_request_failure(self, mock_post):
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        client = CohereClient()
        chat_history = [
            {"role": "User", "message": "hello"},
            {"role": "Chatbot", "message": "hello!"},
        ]
        with self.assertRaises(ValueError) as context:
            client.perform_stream_request("how are you?", chat_history)
        self.assertIn("Server responded with error: 400", str(context.exception))

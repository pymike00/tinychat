import unittest
from unittest.mock import patch, Mock

import requests

from tinychat.llms.cohere import CohereClient


class TestCohereClient(unittest.TestCase):
    @patch("tinychat.llms.cohere.requests.post")
    def test_perform_chat_request_success(self, mock_post):
        assistant_response = "test assistant response"
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": assistant_response}
        mock_post.return_value = mock_response
        client = CohereClient()
        chat_history = [
            {"role": "User", "message": "hello"},
            {"role": "Chatbot", "message": "hello!"},
        ]
        response = client.perform_chat_request("how are you?", chat_history)
        self.assertEqual(response, assistant_response)

    @patch("tinychat.llms.cohere.requests.post")
    def test_perform_chat_request_failure(self, mock_post):
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        client = CohereClient()
        chat_history = [
            {"role": "User", "message": "hello"},
            {"role": "Chatbot", "message": "hello!"},
        ]
        with self.assertRaises(ValueError) as context:
            client.perform_chat_request("how are you?", chat_history)
        self.assertIn("Server responded with error: 400", str(context.exception))

    @patch("tinychat.llms.cohere.requests.post")
    def test_perform_chat_request_invalid_response_format(self, mock_post):
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError
        mock_post.return_value = mock_response
        client = CohereClient()
        chat_history = [
            {"role": "User", "message": "hello"},
            {"role": "Chatbot", "message": "hello!"},
        ]
        with self.assertRaises(ValueError) as context:
            client.perform_chat_request("how are you?", chat_history)
        self.assertIn(
            "Invalid response format received from server.", str(context.exception)
        )


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

import json
import unittest
from unittest.mock import MagicMock, Mock, patch

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


class TestGoogleAIClientStreaming(unittest.TestCase):
    @patch("tinychat.llms.google.requests.post")
    @patch("tinychat.llms.google.SSEClient")
    def test_perform_stream_request_success(self, mock_sse_client, mock_post):
        # Mocking SSEClient and the response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Creating mock events
        mock_event1 = MagicMock()
        mock_event1.data = json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "part1"}]}}]}
        )
        mock_event2 = MagicMock()
        mock_event2.data = json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "part2"}]}}]}
        )
        mock_event_done = MagicMock()
        mock_event_done.data = "[DONE]"

        # Setting up a test stream
        test_stream = [mock_event1, mock_event2, mock_event_done]
        mock_sse_client.return_value.events = MagicMock(return_value=iter(test_stream))

        client = GoogleAIClient()
        messages = [{"parts": [{"text": "content"}], "role": "user"}]
        stream = client.perform_stream_request(messages)

        # Extracting and verifying the stream response
        responses = []
        for event in stream.events():
            if event.data != "[DONE]":
                event_data = json.loads(event.data)
                response_piece = event_data["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                responses.append(response_piece)

        self.assertEqual(responses, ["part1", "part2"])

    @patch("tinychat.llms.google.requests.post")
    def test_perform_stream_request_failure(self, mock_post):
        # Mocking the response with an error status code
        mock_response = Mock(spec=Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        client = GoogleAIClient()
        messages = [{"parts": [{"text": "content"}], "role": "user"}]

        with self.assertRaises(ValueError) as context:
            next(client.perform_stream_request(messages))  # type: ignore
        self.assertIn(
            "Server responded with an error. Status Code: 400", str(context.exception)
        )

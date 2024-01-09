import json
import unittest
from unittest.mock import MagicMock, Mock, patch

from requests.models import Response

from tinychat.llms.mistral import MistralClient


class TestMistralClient(unittest.TestCase):
    @patch("tinychat.llms.mistral.requests.post")
    def test_perform_chat_request_success(self, mock_post):
        assistant_response = "test assistant response"
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"role": "assistant", "content": assistant_response}}
            ]
        }
        mock_post.return_value = mock_response

        client = MistralClient(model_name="test_model")
        messages = [{"role": "user", "content": "hello"}]
        response = client.perform_chat_request(messages)
        self.assertEqual(response, assistant_response)

    @patch("tinychat.llms.mistral.requests.post")
    def test_perform_chat_request_failure(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        client = MistralClient(model_name="test_model")
        messages = [{"role": "user", "content": "hello"}]
        with self.assertRaises(ValueError) as context:
            client.perform_chat_request(messages)
        self.assertIn(
            "Server responded with an error. Status Code: 400", str(context.exception)
        )

    @patch("tinychat.llms.mistral.requests.post")
    def test_perform_chat_request_invalid_response_format(self, mock_post):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"text": "invalid-response-w/-text-key"}
        mock_post.return_value = mock_response

        client = MistralClient(model_name="test_model")
        messages = [{"role": "user", "content": "hello"}]
        with self.assertRaises(KeyError) as context:
            client.perform_chat_request(messages)
        self.assertIn(
            "Invalid response format received from server.", str(context.exception)
        )


class TestMistralClientStreaming(unittest.TestCase):
    @patch("tinychat.llms.mistral.requests.post")
    @patch("tinychat.llms.mistral.SSEClient")
    def test_perform_stream_request_success(self, mock_sse_client, mock_post):
        # Setup: Mocking SSEClient and the response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Creating mock events
        mock_event1 = MagicMock()
        mock_event1.data = json.dumps({"choices": [{"delta": {"content": "part1"}}]})
        mock_event2 = MagicMock()
        mock_event2.data = json.dumps({"choices": [{"delta": {"content": "part2"}}]})
        mock_event_done = MagicMock()
        mock_event_done.data = "[DONE]"

        # Setting up a test stream
        test_stream = [mock_event1, mock_event2, mock_event_done]
        mock_sse_client.return_value.events = MagicMock(return_value=iter(test_stream))

        # Execution
        client = MistralClient(model_name="test_model")
        messages = [{"role": "user", "content": "hello"}]
        stream = client.perform_stream_request(messages)

        # Verification: Extracting and verifying the stream response
        responses = []
        for event in stream.events():
            if event.data != "[DONE]":
                event_data = json.loads(event.data)
                if "choices" in event_data and len(event_data["choices"]) > 0:
                    response_content = event_data["choices"][0]["delta"].get("content", "")
                    responses.append(response_content)

        self.assertEqual(responses, ["part1", "part2"])

    @patch("tinychat.llms.mistral.requests.post")
    def test_perform_stream_request_failure(self, mock_post):
        # Setup: Mocking the response with an error status code
        mock_response = Mock(spec=Response)
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Execution
        client = MistralClient(model_name="test_model")
        messages = [{"role": "user", "content": "hello"}]

        # Verification: Expecting a ValueError on error response
        with self.assertRaises(ValueError) as context:
            next(client.perform_stream_request(messages))  # type: ignore
        self.assertIn(
            "Server responded with an error. Status Code: 400", str(context.exception)
        )
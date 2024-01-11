import unittest
from unittest.mock import patch

from tinychat.llms.cohere import CohereHandler, CohereClient


class TestCohereHandler(unittest.TestCase):
    @patch.object(CohereClient, "perform_chat_request")
    def test_get_response(self, mock_perform_chat_request):
        mock_chat_response = "mock response"
        mock_perform_chat_request.return_value = mock_chat_response
        handler = CohereHandler()
        user_input = "hello"
        response = handler.get_response(user_input)
        self.assertEqual(response, mock_chat_response)
        expected_chat_history = [
            {"role": "User", "message": user_input},
            {"role": "Chatbot", "message": mock_chat_response},
        ]
        self.assertEqual(handler._chat_history, expected_chat_history)


class TestCohereHandlerStreaming(unittest.TestCase):
    @patch.object(CohereClient, "perform_stream_request")
    def test_stream_response(self, mock_perform_stream_request):
        # Create a mock generator to simulate streaming response
        mock_stream = iter(
            [
                "response part 1",
                "response part 2",
                "response part 3"
            ]
        )
        mock_perform_stream_request.return_value = mock_stream

        handler = CohereHandler()
        generator = handler.stream_response("hello")

        # Extracting and verifying the stream response
        responses = []
        for part in generator:
            responses.append(part)

        self.assertEqual(responses, ["response part 1", "response part 2", "response part 3"])
        expected_chat_history = [
            {"role": "User", "message": "hello"},
            {"role": "Chatbot", "message": "response part 1response part 2response part 3"},
        ]
        self.assertEqual(handler._chat_history, expected_chat_history)
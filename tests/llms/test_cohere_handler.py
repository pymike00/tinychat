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
    def test_stream_response_success(self, mock_perform_stream_request):
        # Mocking the stream of responses
        mock_stream = [b'{"event_type": "text-generation", "text": "Hi!"}', 
                       b'{"event_type": "text-generation", "text": "How can I help?"}']
        mock_perform_stream_request.return_value = mock_stream

        handler = CohereHandler()
        user_input = "hello"
        generator = handler.stream_response(user_input)
        
        # Collecting responses from the generator
        responses = [resp for resp in generator]

        # Expected responses and chat history
        expected_responses = ["Hi!", "How can I help?"]
        expected_chat_history = [
            {"role": "User", "message": user_input},
            {"role": "Chatbot", "message": "".join(expected_responses)}
        ]

        self.assertEqual(responses, expected_responses)
        self.assertEqual(handler._chat_history, expected_chat_history)

import unittest
from unittest.mock import patch

from tinychat.llms.google import GoogleGeminiHandler, GoogleGeminiClient


class TestGoogleGeminiHandler(unittest.TestCase):
    @patch.object(GoogleGeminiClient, "perform_chat_request")
    def test_get_response(self, mock_perform_chat_request):
        test_user_input = "hello Bard"
        test_model_response = "hello dear user"
        mock_perform_chat_request.return_value = test_model_response
        handler = GoogleGeminiHandler()
        response = handler.get_response(test_user_input)
        self.assertEqual(response, test_model_response)
        expected_messages = [
            {"parts": [{"text": test_user_input}], "role": "user"},
            {
                "parts": [{"text": test_model_response}],
                "role": "model",
            },
        ]
        self.assertEqual(handler._messages, expected_messages)

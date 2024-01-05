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


if __name__ == "__main__":
    unittest.main()

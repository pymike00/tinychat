import unittest
from unittest.mock import patch

from tinychat.llms.mistral import MistralClient, MistralHandler


class TestMistralHandler(unittest.TestCase):
    @patch.object(MistralClient, "perform_chat_request")
    def test_get_response(self, mock_perform_chat_request):
        mock_perform_chat_request.return_value = "test response"
        handler = MistralHandler(model_name="test_model")
        response = handler.get_response("hello")
        self.assertEqual(response, "test response")
        self.assertEqual(
            handler._messages,
            [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "test response"},
            ],
        )

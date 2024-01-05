import unittest
from unittest.mock import patch

from tinychat.llms.openai import OpenAIClient, OpenAIHandler


class TestOpenAIHandler(unittest.TestCase):

    @patch.object(OpenAIClient, 'perform_chat_request')
    def test_get_response(self, mock_perform_chat_request):
        mock_perform_chat_request.return_value = "test response"
        handler = OpenAIHandler(model_name='test_model')
        response = handler.get_response("hello")
        self.assertEqual(response, "test response")
        self.assertEqual(handler._messages, [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "test response"}
        ])
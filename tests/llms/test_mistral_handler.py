import json
import unittest
from unittest.mock import MagicMock, Mock, patch

from tinychat.llms.mistral import MistralClient, MistralHandler


class TestMistralHandlerStreaming(unittest.TestCase):
    @patch.object(MistralClient, "perform_stream_request")
    def test_stream_response(self, mock_perform_stream_request):
        # Create a mock SSEClient with a mock events method
        mock_sse_client = MagicMock()
        mock_stream = iter(
            [
                Mock(
                    data=json.dumps(
                        {"choices": [{"delta": {"content": "response part 1"}}]}
                    )
                ),
                Mock(
                    data=json.dumps(
                        {"choices": [{"delta": {"content": "response part 2"}}]}
                    )
                ),
                Mock(data="[DONE]"),
            ]
        )
        mock_sse_client.events.return_value = mock_stream
        mock_perform_stream_request.return_value = mock_sse_client

        handler = MistralHandler(model_name="test_model")
        generator = handler.stream_response("hello")

        # Extracting and verifying the stream response
        responses = []
        for part in generator:
            responses.append(part)

        self.assertEqual(responses, ["response part 1", "response part 2"])
        self.assertEqual(
            handler._messages,
            [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "response part 1response part 2"},
            ],
        )

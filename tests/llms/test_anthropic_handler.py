import json
import unittest
from unittest.mock import MagicMock, Mock, patch

from tinychat.llms.anthropic import AnthropicAIClient, AnthropicAIHandler


class TestAnthropicAIHandlerStreaming(unittest.TestCase):
    # TODO: improve
    @patch.object(AnthropicAIClient, "perform_stream_request")
    @patch("tinychat.llms.base.BaseLLMClient.api_key", new_callable=MagicMock)
    def test_stream_response_success(self, mock_api_key, mock_perform_stream_request):
        # Setting a dummy value for mock_api_key is not strictly needed here

        # Create a mock SSEClient with a mock events method
        mock_sse_client = MagicMock()
        mock_stream = iter(
            [
                Mock(
                    data=json.dumps(
                        {
                            "type": "content_block_start",
                            "index": 0,
                            "content_block": {"type": "text", "text": ""},
                        }
                    )
                ),
                Mock(data=json.dumps({"type": "ping"})),
                Mock(
                    data=json.dumps(
                        {
                            "type": "content_block_delta",
                            "index": 0,
                            "delta": {"type": "text_delta", "text": "Hello"},
                        }
                    )
                ),
                Mock(
                    data=json.dumps(
                        {
                            "type": "content_block_delta",
                            "index": 0,
                            "delta": {"type": "text_delta", "text": "!"},
                        }
                    )
                ),
                Mock(data=json.dumps({"type": "content_block_stop", "index": 0})),
            ]
        )
        mock_sse_client.events.return_value = mock_stream
        mock_perform_stream_request.return_value = mock_sse_client

        handler = AnthropicAIHandler(model_name="test_model")
        generator = handler.stream_response("hello")

        # Extracting and verifying the stream response
        responses = []
        for part in generator:
            responses.append(part)

        self.assertEqual(responses, ["Hello", "!"])
        self.assertEqual(
            handler._messages,
            [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "Hello!"},
            ],
        )

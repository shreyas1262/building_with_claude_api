from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()  # Load environment variables from .env file
client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

class MessageHelper():
    """Helper for building conversations and sending them to the Claude API.

    Attributes:
        model: ID of the Claude model used for every request.
    """

    def __init__(self):
        self.model = "claude-haiku-4-5-20251001"

    def add_user_message(self, messages: list[dict], text: str) -> list[dict]:
        """Append a user turn to the conversation.

        Args:
            messages: List of message dicts (`{"role": ..., "content": ...}`),
                modified in place.
            text: The user's message text.

        Returns:
            The same `messages` list, so calls can be chained.
        """
        messages.append({"role": "user", "content": text})
        return messages

    def add_assistant_message(self, messages: list[dict], text: str) -> list[dict]:
        """Append an assistant turn to the conversation.

        Used both to replay earlier Claude replies and to prefill the start of
        Claude's next response (when it is the last message sent).

        Args:
            messages: List of message dicts (`{"role": ..., "content": ...}`),
                modified in place.
            text: The assistant's message text, or the prefill text.

        Returns:
            The same `messages` list, so calls can be chained.
        """
        messages.append({"role": "assistant", "content": text})
        return messages

    def chat(self, messages: list[dict], system: str = None, stop_sequences: list[str] = None, max_tokens: int = 1000) -> str:
        """Send the conversation to Claude and return its text reply.

        Args:
            messages: List of message dicts representing the conversation so
                far. If the last message is from the assistant, Claude
                continues from that text (prefill).
            system: Optional system prompt (str) that sets Claude's behavior.
                Omitted from the request when None or empty.
            stop_sequences: Optional list of strings; generation stops as soon
                as Claude would produce one, and the stop string itself is not
                included in the returned text. Omitted when None or empty.
            max_tokens: Maximum number of tokens (int) Claude may generate;
                longer replies are cut off. Defaults to 1000.

        Returns:
            The text of Claude's first content block (str).
        """
        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }

        # Optional parameters are only added when provided, since the API
        # rejects empty/None values for them.
        if system:
            params["system"] = system
        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        response = client.messages.create(**params)
        # The reply is a list of content blocks; plain replies have a single
        # text block at index 0.
        return response.content[0].text

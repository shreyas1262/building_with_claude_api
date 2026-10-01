---
name: comment-python
description: Add explanatory comments and docstrings to a Python file. Use when the user asks to comment, document, or add docstrings to Python classes and functions.
---

# Comment Python

Read the whole target file first, so comments reflect how each piece is actually used. Then add comments. Never change code behavior, names, imports, or formatting; only add or improve comments and docstrings.

If the user doesn't name a file, ask which one (or use the file they have open).

## What to write

**Classes**: add a docstring directly under the `class` line saying what the class represents or does, and what it is used for. Mention important attributes set in `__init__` (e.g. `model`: the Claude model ID used for requests).

**Functions and methods**: add a docstring directly under the `def` line with:
1. A one-line summary of what the function does.
2. `Args:` listing every parameter (skip `self`/`cls`) with what it is and how it is used. Include the expected type, and say so when it is optional and what its default means.
3. `Returns:` describing what comes back, including the type. Omit if the function returns nothing.
4. `Raises:` only if the function raises exceptions deliberately.

**Complex operations**: add a short inline `#` comment above any line or block that isn't obvious at a glance. Examples: nested comprehensions, regexes, slicing or index tricks, mutation of an argument in place, conditional parameter building, API-specific behavior (e.g. why a prefill or stop sequence is used). Explain the *why*, not a restatement of the code.

## Style

- Use Google-style docstrings with triple double-quotes.
- Match the file's existing indentation and any comments already there; keep useful existing comments and don't duplicate them.
- Keep it short. One-line docstrings are fine for trivial functions; the `Args:` section is still required if there are parameters.
- Don't comment self-explanatory lines (`x = x + 1`, plain assignments, simple returns).
- Describe what the code does today, not what it should do. If you spot a bug or odd behavior, mention it to the user in your reply instead of hiding it in a comment.

## Example

Before:
```python
class MessageHelper():
    def __init__(self):
        self.model = "claude-haiku-4-5-20251001"

    def add_user_message(self, messages, text):
        messages.append({"role": "user", "content": text})
        return messages
```

After:
```python
class MessageHelper():
    """Helper for building conversations and sending them to the Claude API.

    Attributes:
        model: ID of the Claude model used for every request.
    """

    def __init__(self):
        self.model = "claude-haiku-4-5-20251001"

    def add_user_message(self, messages, text):
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
```

## After editing

Reply with a brief summary of what was commented, and list anything suspicious you noticed but did not change.

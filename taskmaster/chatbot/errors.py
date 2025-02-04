class ChatBotError(Exception):
    """Base class for exceptions in this module."""


class MessageTooLongError(ChatBotError):
    """Raised when a message exceeds the maximum length."""

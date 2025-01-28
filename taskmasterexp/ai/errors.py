class AiAssistantError(Exception):
    """Base class for exceptions in this module."""


class MessageTooLongError(AiAssistantError):
    """Raised when a message exceeds the maximum length."""

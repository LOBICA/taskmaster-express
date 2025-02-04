"""Define exceptios for twilio integration"""


class TwilioError(Exception):
    """Base exception for twilio integrations."""


class MessageTooLongError(TwilioError):
    """Raised when a message exceeds the maximum length."""

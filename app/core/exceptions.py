"""
Custom exception hierarchy for Argus ANPR domain and service errors.

These exceptions map cleanly to HTTP status codes at the API layer:
  - ANPRServiceError: Base service error (default 500)
  - InvalidImageError: Client sent unparseable or unsupported image data (400)
"""


class ANPRServiceError(Exception):
    """Base exception for ANPR domain errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InvalidImageError(ANPRServiceError):
    """Raised when an input file is not a valid or supported image."""

    def __init__(self, message: str = "Invalid or unsupported image file"):
        super().__init__(message=message, status_code=400)

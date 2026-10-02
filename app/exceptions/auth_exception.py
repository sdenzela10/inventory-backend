class AuthenticationError(Exception):
    """Base exception for authentication failures."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when authentication credentials are invalid."""


class InvalidTokenError(AuthenticationError):
    """Raised when an authentication token is invalid or expired."""
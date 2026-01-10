class DomainException(Exception):
    pass


class AuthenticationError(DomainException):
    pass


class InvalidTokenError(AuthenticationError):
    pass


class UserNotFoundError(DomainException):
    pass


class InvalidCredentialsError(AuthenticationError):
    pass


class ServiceUnavailableError(DomainException):
    pass


class YandexServiceError(ServiceUnavailableError):
    pass

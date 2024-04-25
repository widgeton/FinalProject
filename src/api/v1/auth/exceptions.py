class AuthException(Exception):
    pass


class TokenDataException(AuthException):
    pass


class SendEmailMessageException(AuthException):
    pass


class RegisterCompanyException(AuthException):
    pass

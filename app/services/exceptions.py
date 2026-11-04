class ServiceError(Exception):
 pass


class UsernameAlreadyExistsException(ServiceError):
 pass


class InvalidCredentialsException(ServiceError):
 pass

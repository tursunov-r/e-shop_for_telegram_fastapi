class PermissionDeniedError(Exception):
    pass


class NotAuthorized(Exception):
    pass


class Forbidden(Exception):
    pass


class NotFound(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class ProductAlreadyExists(Exception):
    pass

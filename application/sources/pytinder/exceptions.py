class PytinderError(Exception):
    pass


class RequestError(PytinderError):
    pass


class InitializationError(PytinderError):
    pass


class RecsError(PytinderError):
    pass


class RecsTimeout(RecsError):
    pass


class UserError(Exception):
    pass


class UserInitializationError(UserError):
    pass


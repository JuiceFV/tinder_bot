"""The module contains some Exceptions classes.
The tinder's API could raise an exception.
Here represented some classes responsible for handling them.
"""


class PytinderError(Exception):
    """Base exception class
    """
    pass


class RequestError(PytinderError):
    """Exception which is called when a request
    to the Tinder is failed.
    """
    pass


class InitializationError(PytinderError):
    """Exception when initialization of a session went wrong.
    """
    pass


class RecsError(PytinderError):
    """Exception of recommendation.
    """
    pass


class RecsTimeout(RecsError):
    """Exception when the recommendation response time is out.
    """
    pass


class UserError(Exception):
    """Exception with the user's class
    """
    pass


class UserInitializationError(UserError):
    """Exception with the user's initialization.
    """
    pass


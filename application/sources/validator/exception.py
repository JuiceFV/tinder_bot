"""This module represent the base exception's classes
"""


class CanvasError(Exception):
    """The base canvas exception.
    """
    pass


class ImagesNotFound(CanvasError):
    """Arise if image hasn't been found.
    """
    pass


class UndefinedBehaviorOfImageDefinition(CanvasError):
    """Arise when something with image definition went wrong.
    """
    pass


class ImagesAlreadyDefined(CanvasError):
    """Arise when image image already defined.
    """
    pass


class VoteError(Exception):
    """Arise when something with vote went wrong.
    """
    pass


class VoteDefinition(VoteError):
    """Arise when something with vote definition went wrong.
    """
    pass


class DecisionError(Exception):
    """Arise when something with decision went wrong.
    """
    pass

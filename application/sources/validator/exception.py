class CanvasError(Exception):
    pass


class ImagesNotFound(CanvasError):
    pass


class UndefinedBehaviorOfImageDefinition(CanvasError):
    pass


class ImagesAlreadyDefined(CanvasError):
    pass


class VoteError(Exception):
    pass


class VoteDefinition(VoteError):
    pass


class DecisionError(Exception):
    pass

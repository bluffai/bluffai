class InvalidEventError(Exception):
    pass


class InvalidPotError(Exception):
    pass


class InvalidStateError(Exception):
    pass


def validate_event(predicate: bool, description: str):
    if not predicate:
        raise InvalidEventError(description)


def validate_pot(predicate: bool, description: str):
    if not predicate:
        raise InvalidPotError(description)


def validate_state(predicate: bool, description: str):
    if not predicate:
        raise InvalidStateError(description)

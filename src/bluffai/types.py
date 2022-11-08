from dataclasses import dataclass
from enum import Enum, auto, unique

from bluffai.validate import validate_pot

RandomSeed = int | float | str | bytes | bytearray | None
"""
A seed value for a pseudo-random number generator.
"""

PlayerID = str
"""
A unique ID of a poker player in a `Room`.
"""

NumChips = int
"""
A number of chips.
"""


class Event:
    pass


class State:
    pass


class Action:
    pass


@unique
class Card(Enum):
    CLUBS_2 = auto()
    CLUBS_3 = auto()
    CLUBS_4 = auto()
    CLUBS_5 = auto()
    CLUBS_6 = auto()
    CLUBS_7 = auto()
    CLUBS_8 = auto()
    CLUBS_9 = auto()
    CLUBS_10 = auto()
    CLUBS_JACK = auto()
    CLUBS_QUEEN = auto()
    CLUBS_KING = auto()
    CLUBS_ACE = auto()
    DIAMONDS_2 = auto()
    DIAMONDS_3 = auto()
    DIAMONDS_4 = auto()
    DIAMONDS_5 = auto()
    DIAMONDS_6 = auto()
    DIAMONDS_7 = auto()
    DIAMONDS_8 = auto()
    DIAMONDS_9 = auto()
    DIAMONDS_10 = auto()
    DIAMONDS_JACK = auto()
    DIAMONDS_QUEEN = auto()
    DIAMONDS_KING = auto()
    DIAMONDS_ACE = auto()
    HEARTS_2 = auto()
    HEARTS_3 = auto()
    HEARTS_4 = auto()
    HEARTS_5 = auto()
    HEARTS_6 = auto()
    HEARTS_7 = auto()
    HEARTS_8 = auto()
    HEARTS_9 = auto()
    HEARTS_10 = auto()
    HEARTS_JACK = auto()
    HEARTS_QUEEN = auto()
    HEARTS_KING = auto()
    HEARTS_ACE = auto()
    SPADES_2 = auto()
    SPADES_3 = auto()
    SPADES_4 = auto()
    SPADES_5 = auto()
    SPADES_6 = auto()
    SPADES_7 = auto()
    SPADES_8 = auto()
    SPADES_9 = auto()
    SPADES_10 = auto()
    SPADES_JACK = auto()
    SPADES_QUEEN = auto()
    SPADES_KING = auto()
    SPADES_ACE = auto()


Deck = tuple[Card, ...]


@dataclass
class Pot:
    player_ids: list[PlayerID]
    player_chips: NumChips

    def __post_init__(self) -> None:
        validate_pot(
            len(self.player_ids) >= 2,
            "The number of players must be greater than or equal to 2.",
        )
        validate_pot(
            self.player_chips > 0,
            "The number of chips per player must be positive.",
        )

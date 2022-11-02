from dataclasses import dataclass

from . import Deck, NumChips, PlayerID
from .state import PlayerPosition


@dataclass
class PlayerBuysIn:
    player_id: PlayerID
    player_stack: NumChips


@dataclass
class StartHand:
    pass


@dataclass
class SetBlinds:
    big_blind: NumChips
    little_blind: NumChips
    big_blind_position: PlayerPosition
    little_blind_position: PlayerPosition


@dataclass
class PlaceBlinds:
    pass


@dataclass
class ShuffleDeck:
    deck: Deck


@dataclass
class DealHoleCards:
    pass


@dataclass
class PlayerCalls:
    player_id: PlayerID


@dataclass
class PlayerRaises:
    player_id: PlayerID


@dataclass
class PlayerFolds:
    player_id: PlayerID

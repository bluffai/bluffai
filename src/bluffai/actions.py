from dataclasses import dataclass

from bluffai.types import Action, Deck, NumChips, PlayerID


@dataclass(frozen=True, kw_only=True)
class PlayerBuysIn(Action):
    player_id: PlayerID
    player_stack: NumChips


@dataclass(frozen=True, kw_only=True)
class StartHand(Action):
    hand_player_ids: tuple[PlayerID, ...]


@dataclass(frozen=True, kw_only=True)
class SetBlinds(Action):
    little_blind: NumChips
    big_blind: NumChips


@dataclass(frozen=True, kw_only=True)
class PlaceBlinds(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class ShuffleDeck(Action):
    deck: Deck


@dataclass(frozen=True, kw_only=True)
class DealHoleCards(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class PlayerCalls(Action):
    player_id: PlayerID
    bet: NumChips


@dataclass(frozen=True, kw_only=True)
class PlayerRaises(Action):
    player_id: PlayerID
    bet: NumChips


@dataclass(frozen=True, kw_only=True)
class PlayerFolds(Action):
    player_id: PlayerID


@dataclass(frozen=True, kw_only=True)
class PlayerChecks(Action):
    player_id: PlayerID


@dataclass(frozen=True, kw_only=True)
class DeclareDefaultWinner(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class FinishPreFlopBetting(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class DealFlopCards(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class FinishPostFlopBetting(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class DealTurnCard(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class FinishPostTurn(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class DealRiverCard(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class FinishPostRiverBetting(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class PlayerRevealsHand(Action):
    player_id: PlayerID


@dataclass(frozen=True, kw_only=True)
class RankHands(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class DistributePots(Action):
    pass


@dataclass(frozen=True, kw_only=True)
class EndGame(Action):
    pass

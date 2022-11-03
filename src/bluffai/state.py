from dataclasses import dataclass
from typing import Tuple

from . import Card, Deck, NumChips, PlayerID

StateType = str
PlayerPosition = int
Pot = dict[PlayerID, NumChips]


class InvalidStateError(Exception):
    pass


def validate_state(predicate: bool, description: str):
    if not predicate:
        raise InvalidStateError(description)


class State:
    pass


@dataclass
class BuyingIn(State):
    """
    No previous states.

    Next states:
        * PlayerBuysIn -> BuyingIn
        * StartHand -> SettingBlinds
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack > 0 for player_stack in self.player_stacks]),
            "Every player must have a postive stack.",
        )


@dataclass
class SettingBlinds(State):
    """
    Previous states:
        * BuyingIn -> StartHand

    Next states:
        * SetBlinds -> PlacingBlinds
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )


@dataclass
class PlacingBlinds(State):
    """
    Previous states:
        * SettingBlinds -> SetBlinds

    Next states:
        * PlaceBlinds -> ShufflingDeck
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")


@dataclass
class ShuffleDeck(State):
    """
    Previous states:
        * PlacingBlinds -> PlaceBlinds

    Next states:
        * ShuffleDeck -> DealingHoleCards
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)] > 0
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(
            len(self.hand_player_bets) == len(self.hand_player_ids),
            "Every player in the hand must have a bet.",
        )
        validate_state(
            all([hand_player_bet >= 0 for hand_player_bet in self.hand_player_bets]),
            "Every player in the hand must have a non-negative bet.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(hand_player_id)]
                    >= hand_player_bet
                    for hand_player_id, hand_player_bet in zip(
                        self.hand_player_ids, self.hand_player_bets
                    )
                ]
            ),
            "Every player in the hand must have a stack that is greater than or equal "
            "to their bet.",
        )
        validate_state(
            self.hand_player_bets[0] == self.big_blind
            or self.hand_player_bets[0]
            == self.player_stacks[self.player_ids.index(self.hand_player_ids[1])],
            "The player in the little blind position must have a bet that is equal to "
            "the little blind or be all-in.",
        )
        validate_state(
            self.hand_player_bets[1] == self.big_blind
            or self.hand_player_bets[1]
            == self.player_stacks[self.player_ids.index(self.hand_player_ids[1])],
            "The player in the big blind position must have a bet that is equal to the "
            "big blind or be all-in.",
        )
        validate_state(
            all(
                [hand_player_bet == 0 for hand_player_bet in self.hand_player_bets[2:]]
            ),
            "Every player in the hand who is not in the little blind position and is "
            "not in the big blind position must have a bet of 0.",
        )


@dataclass
class DealingHoldCards(State):
    """
    Previous states:
        * ShufflingDeck -> ShuffleDeck

    Next states:
        * DealHoleCards -> PreFlopBetting
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]
    deck: Deck

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)] > 0
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(
            len(self.hand_player_bets) == len(self.hand_player_ids),
            "Every player in the hand must have a bet.",
        )
        validate_state(
            all([hand_player_bet >= 0 for hand_player_bet in self.hand_player_bets]),
            "Every player in the hand must have a non-negative bet.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(hand_player_id)]
                    >= hand_player_bet
                    for hand_player_id, hand_player_bet in zip(
                        self.hand_player_ids, self.hand_player_bets
                    )
                ]
            ),
            "Every player in the hand must have a stack that is greater than or equal "
            "to their bet.",
        )
        validate_state(
            self.hand_player_bets[0] == self.big_blind
            or self.hand_player_bets[0]
            == self.player_stacks[self.player_ids.index(self.hand_player_ids[1])],
            "The player in the little blind position must have a bet that is equal to "
            "the little blind or be all-in.",
        )
        validate_state(
            self.hand_player_bets[1] == self.big_blind
            or self.hand_player_bets[1]
            == self.player_stacks[self.player_ids.index(self.hand_player_ids[1])],
            "The player in the big blind position must have a bet that is equal to the "
            "big blind or be all-in.",
        )
        validate_state(
            all(
                [hand_player_bet == 0 for hand_player_bet in self.hand_player_bets[2:]]
            ),
            "Every player in the hand who is not in the little blind position and is "
            "not in the big blind position must have a bet of 0.",
        )
        validate_state(len(self.deck) == 52, "The deck must have 52 cards.")


@dataclass
class PreFlopBetting(State):
    """
    Previous states:
        * DealingHoleCards -> DealHoleCards

    Next states:
        * PlayerCalls -> PreFlopBetting
        * PlayerRaises -> PreFlopBetting
        * PlayerFolds -> PreFlopBetting
        * FinishPreFlopBetting -> DealingFlopCards
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]
    deck: Deck
    hand_player_hold_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)] > 0
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(
            len(self.hand_player_bets) == len(self.hand_player_ids),
            "Every player in the hand must have a bet.",
        )
        validate_state(
            all([hand_player_bet >= 0 for hand_player_bet in self.hand_player_bets]),
            "Every player in the hand must have a non-negative bet.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(hand_player_id)]
                    >= hand_player_bet
                    for hand_player_id, hand_player_bet in zip(
                        self.hand_player_ids, self.hand_player_bets
                    )
                ]
            ),
            "Every player in the hand must have a stack that is greater than or equal "
            "to their bet.",
        )
        validate_state(
            len(self.deck) == 52 - 2 * len(self.hand_player_ids),
            "The deck must have 52 cards minus 2 cards for each player in the hand.",
        )
        validate_state(
            len(self.hand_player_hold_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least one player in the hand must not have folded.",
        )


@dataclass
class DealingFlopCards(State):
    """
    Previous states:
        * PreFlopBetting -> FinishPreFlopBetting

    Next states:
        * DealFlopCards -> PostFlopBetting
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]
    deck: Deck
    hand_player_hold_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]

    def __post_init__(self) -> None:
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)] >= 0
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a non-negative stack.",
        )
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(
            len(self.hand_player_bets) == len(self.hand_player_ids),
            "Every player in the hand must have a bet.",
        )
        validate_state(
            all([hand_player_bet == 0 for hand_player_bet in self.hand_player_bets]),
            "Every player in the hand must have a bet equal to 0.",
        )
        validate_state(
            len(self.deck) == 52 - 2 * len(self.hand_player_ids),
            "The deck must have 52 cards minus 2 cards for each player in the hand.",
        )
        validate_state(
            len(self.hand_player_hold_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least one player in the hand must not have folded.",
        )
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    all([player_stake > 0 for player_stake in pot.values()])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player must have a positive stake.",
        )
        validate_state(
            all(
                [
                    all([player_stake > 0 for player_stake in pot.values()])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player must have a positive stake.",
        )


# Pots
# After a betting round, there may be multiple pots (a.k.a. side pots).
# In each side pot, there are a set of players who contributed to the side pot
# and a fixed contribution to the side pot by each player.
# Thus, we can represent a side pot as a tuple [list(player_id), player_chips]
#
# In the example:
# PlayerA: 100, not folded, not all-in
# PlayerB: 80, folded, not all-in
# PlayerC: 90, not folded, all-in
# PlayerD: 100, not folded, not all-in
# PlayerE: 95, folded, not all-in
# PlayerF: 50, not folded, all-in
#
# We have the following pots:
#
# Pot 1:
# PlayerA: 50
# PlayerB: 50 (folded)
# PlayerC: 50
# PlayerD: 50
# PlayerE: 50 (folded)
# PlayerF: 50
#
# Pot 2:
# PlayerA: 30
# PlayerB: 30 (folded)
# PlayerC: 30
# PlayerD: 30
# PlayerE: 30 (folded)
#
# Pot 3:
# PlayerA: 10
# PlayerC: 10
# PlayerD: 10
# PlayerE: 10 (folded)
#
# Pot 4:
# PlayerA: 5
# PlayerD: 5
# PlayerE: 5 (folded)
#
# Pot 5:
# PlayerA: 5
# PlayerD: 5

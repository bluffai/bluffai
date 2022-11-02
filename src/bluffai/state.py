from dataclasses import dataclass
from typing import Tuple

from . import Card, Deck, NumChips, PlayerID

StateType = str
PlayerPosition = int


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
    # TODO: Refactor states to use hand_* state instead of big_blind_position, etc.

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
            len(self.player_ids_in_hand) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all(
                [player_id in self.player_ids for player_id in self.player_ids_in_hand]
            ),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.player_ids_in_hand
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
    player_ids_in_hand: list[PlayerID]
    big_blind: NumChips
    little_blind: NumChips

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
            len(self.player_ids_in_hand) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all(
                [player_id in self.player_ids for player_id in self.player_ids_in_hand]
            ),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.player_ids_in_hand
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(self.little_blind > 0, "The little blind must be positive.")


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
    player_ids_in_hand: list[PlayerID]
    big_blind: NumChips
    little_blind: NumChips
    player_bets: list[NumChips]

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
            len(self.player_ids_in_hand) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all(
                [player_id in self.player_ids for player_id in self.player_ids_in_hand]
            ),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.player_ids_in_hand
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(
            len(self.player_bets) == len(self.player_ids),
            "Every player must have a bet.",
        )
        validate_state(
            all([player_bet >= 0 for player_bet in self.player_bets]),
            "Every player must have a non-negative bet.",
        )
        validate_state(
            all(
                [
                    player_bet <= player_stack
                    for player_bet, player_stack in zip(
                        self.player_bets, self.player_stacks
                    )
                ]
            ),
            "Every player must have a bet that is less than or equal to their stack.",
        )
        validate_state(
            self.player_bets[self.big_blind_position] == self.big_blind
            or self.player_bets[self.big_blind_position]
            == self.player_stacks[self.big_blind_position],
            "The player in the big blind position must have a bet that is equal to the "
            "big blind or be all-in.",
        )
        validate_state(
            self.player_bets[self.little_blind_position] == self.little_blind
            or self.player_bets[self.little_blind_position]
            == self.player_stacks[self.little_blind_position],
            "The player in the little blind position must have a bet that is equal to "
            "the little blind or be all-in.",
        )
        validate_state(
            all(
                [
                    player_bet == 0
                    for player_position, player_bet in enumerate(self.player_bets)
                    if player_position != self.big_blind_position
                    and player_position != self.little_blind_position
                ]
            ),
            "Every player who is not in the big blind position and is not in the "
            "little blind position must have a bet of 0.",
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
    player_ids_in_hand: list[PlayerID]
    big_blind: NumChips
    little_blind: NumChips
    player_bets: list[NumChips]
    deck: Deck

    def __post_init__(self) -> None:
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
            len(self.player_ids_in_hand) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all(
                [player_id in self.player_ids for player_id in self.player_ids_in_hand]
            ),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.player_ids_in_hand
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(
            0 <= self.big_blind_position <= len(self.player_ids),
            "The big blind position must be in range of the number of players.",
        )
        validate_state(
            self.player_stacks[self.big_blind_position] > 0,
            "The player in the big blind position must have a positive stack.",
        )
        validate_state(
            0 <= self.little_blind_position <= len(self.player_ids),
            "The little blind position must be in range of the number of players.",
        )
        validate_state(
            self.player_stacks[self.little_blind_position] > 0,
            "The player in the little blind position must have a positive stack.",
        )
        validate_state(
            self.big_blind_position != self.little_blind_position,
            "The big blind position must be different from the little blind position.",
        )
        player_position = (self.little_blind_position + 1) % len(self.player_ids)
        while player_position != self.big_blind_position:
            validate_state(
                self.player_stacks[player_position] == 0,
                "Any player between the player in the little blind position and the "
                "player in the big blind position must have a stack of 0.",
            )
            player_position = (player_position + 1) % len(self.player_ids)
        validate_state(
            len(self.player_bets) == len(self.player_ids),
            "Every player must have a bet.",
        )
        validate_state(
            all([player_bet >= 0 for player_bet in self.player_bets]),
            "Every player must have a non-negative bet.",
        )
        validate_state(
            all(
                [
                    player_bet <= player_stack
                    for player_bet, player_stack in zip(
                        self.player_bets, self.player_stacks
                    )
                ]
            ),
            "Every player must have a bet that is less than or equal to their stack.",
        )
        validate_state(
            self.player_bets[self.big_blind_position] == self.big_blind
            or self.player_bets[self.big_blind_position]
            == self.player_stacks[self.big_blind_position],
            "The player in the big blind position must have a bet that is equal to the "
            "big blind or be all-in.",
        )
        validate_state(
            self.player_bets[self.little_blind_position] == self.little_blind
            or self.player_bets[self.little_blind_position]
            == self.player_stacks[self.little_blind_position],
            "The player in the little blind position must have a bet that is equal to "
            "the little blind or be all-in.",
        )
        validate_state(
            all(
                [
                    player_bet == 0
                    for player_position, player_bet in enumerate(self.player_bets)
                    if player_position != self.big_blind_position
                    and player_position != self.little_blind_position
                ]
            ),
            "Every player who is not in the big blind position and is not in the "
            "little blind position must have a bet of 0.",
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
    player_ids_in_hand: list[PlayerID]
    big_blind: NumChips
    little_blind: NumChips
    player_bets: list[NumChips]
    deck: Deck
    player_hold_cards: list[Tuple[Card, Card]]

    def __post_init__(self) -> None:
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
            len(self.player_ids_in_hand) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all(
                [player_id in self.player_ids for player_id in self.player_ids_in_hand]
            ),
            "Every player in the hand must be a player in the game.",
        )
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.player_ids_in_hand
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )
        validate_state(self.big_blind > 0, "The big blind must be positive.")
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(
            0 <= self.big_blind_position <= len(self.player_ids),
            "The big blind position must be in range of the number of players.",
        )
        validate_state(
            self.player_stacks[self.big_blind_position] > 0,
            "The player in the big blind position must have a positive stack.",
        )
        validate_state(
            0 <= self.little_blind_position <= len(self.player_ids),
            "The little blind position must be in range of the number of players.",
        )
        validate_state(
            self.player_stacks[self.little_blind_position] > 0,
            "The player in the little blind position must have a positive stack.",
        )
        validate_state(
            self.big_blind_position != self.little_blind_position,
            "The big blind position must be different from the little blind position.",
        )
        player_position = (self.little_blind_position + 1) % len(self.player_ids)
        while player_position != self.big_blind_position:
            validate_state(
                self.player_stacks[player_position] == 0,
                "Any player between the player in the little blind position and the "
                "player in the big blind position must have a stack of 0.",
            )
            player_position = (player_position + 1) % len(self.player_ids)
        validate_state(
            len(self.player_bets) == len(self.player_ids),
            "Every player must have a bet.",
        )
        validate_state(
            all([player_bet >= 0 for player_bet in self.player_bets]),
            "Every player must have a non-negative bet.",
        )
        validate_state(
            all(
                [
                    player_bet <= player_stack
                    for player_bet, player_stack in zip(
                        self.player_bets, self.player_stacks
                    )
                ]
            ),
            "Every player must have a bet that is less than or equal to their stack.",
        )
        validate_state(
            self.player_bets[self.big_blind_position] == self.big_blind
            or self.player_bets[self.big_blind_position]
            == self.player_stacks[self.big_blind_position],
            "The player in the big blind position must have a bet that is equal to the "
            "big blind or be all-in.",
        )
        validate_state(
            self.player_bets[self.little_blind_position] == self.little_blind
            or self.player_bets[self.little_blind_position]
            == self.player_stacks[self.little_blind_position],
            "The player in the little blind position must have a bet that is equal to "
            "the little blind or be all-in.",
        )
        validate_state(
            all(
                [
                    player_bet == 0
                    for player_position, player_bet in enumerate(self.player_bets)
                    if player_position != self.big_blind_position
                    and player_position != self.little_blind_position
                ]
            ),
            "Every player who is not in the big blind position and is not in the "
            "little blind position must have a bet of 0.",
        )
        validate_state(
            len(self.deck) == 52,
            "The deck must have 52 cards minus 2 cards for each player.",
        )

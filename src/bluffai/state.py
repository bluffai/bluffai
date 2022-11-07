from dataclasses import dataclass
from typing import Tuple

from . import Card, NumChips, PlayerID

StateType = str
PlayerPosition = int
Deck = list[Card]


class InvalidPotError(Exception):
    pass


def validate_pot(predicate: bool, description: str):
    if not predicate:
        raise InvalidPotError(description)


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
        * EndGame -> GameOver
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
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
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )

        # Validate stacks of players in the hand.
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
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )

        # Validate stacks of players in the hand.
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)]
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )

        # Validate blinds.
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
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )

        # Validate stacks of players in the hand.
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)] > 0
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate bets of players in the hand.
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
            == self.player_stacks[self.player_ids.index(self.hand_player_ids[0])],
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
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
        validate_state(
            len(self.hand_player_ids) >= 2,
            "The number of players in the the hand must be greater than or equal to 2.",
        )
        validate_state(
            all([player_id in self.player_ids for player_id in self.hand_player_ids]),
            "Every player in the hand must be a player in the game.",
        )

        # Validate stacks of players in the hand.
        validate_state(
            all(
                [
                    self.player_stacks[self.player_ids.index(player_id)] > 0
                    for player_id in self.hand_player_ids
                ]
            ),
            "Every player in the hand must have a positive stack.",
        )

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate bets of players in the hand.
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
            == self.player_stacks[self.player_ids.index(self.hand_player_ids[0])],
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

        # Validate cards in the hand.
        hand_cards = self.deck.copy()
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )


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
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate bets of players in the hand.
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

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
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
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )


@dataclass
class PostFlopBetting(State):
    """
    Previous states:
        * DealingFlopCards -> DealFlopCards

    Next states:
        * PlayerCalls -> PostFlopBetting
        * PlayerRaises -> PostFlopBetting
        * PlayerFolds -> PostFlopBetting
        * FinishPostFlopBetting -> DealingTurnCard
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]
    flop_cards: Tuple[Card, Card, Card]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate bets of players in the game.
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

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        hand_cards.extend(self.flop_cards)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )


@dataclass
class DealingTurnCard(State):
    """
    Previous states:
        * PostFlopBetting -> FinishPostFlopBetting

    Next states:
        * DealTurnCard -> PostTurnBetting
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]
    flop_cards: Tuple[Card, Card, Card]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )


@dataclass
class PostTurnBetting(State):
    """
    Previous states:
        * DealingTurnCard -> DealTurnCard

    Next states:
        * PlayerCalls -> PostTurnBetting
        * PlayerRaises -> PostTurnBetting
        * PlayerFolds -> PostTurnBetting
        * FinishPostTurnBetting -> DealingRiverCard
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]
    flop_cards: Tuple[Card, Card, Card]
    turn_card: Card

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate bets of players in the game.
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

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        hand_cards.extend(self.flop_cards)
        hand_cards.append(self.turn_card)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )


@dataclass
class DealingRiverCard(State):
    """
    Previous states:
        * PostTurnBetting -> FinishPostTurnBetting

    Next states:
        * DealRiverCard -> PostRiverBetting
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]
    flop_cards: Tuple[Card, Card, Card]
    turn_card: Card

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        hand_cards.extend(self.flop_cards)
        hand_cards.append(self.turn_card)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )


@dataclass
class PostRiverBetting(State):
    """
    Previous states:
        * DealingRiverCard -> DealRiverCard

    Next states:
        * PlayerCalls -> PostRiverBetting
        * PlayerRaises -> PostRiverBetting
        * PlayerFolds -> PostRiverBetting
        * FinishPostRiverBetting -> Showdown
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: list[NumChips]
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]
    flop_cards: Tuple[Card, Card, Card]
    turn_card: Card
    river_card: Card

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate blinds.
        validate_state(self.little_blind > 0, "The little blind must be positive.")
        validate_state(self.big_blind > 0, "The big blind must be positive.")

        # Validate bets of players in the game.
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

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        hand_cards.extend(self.flop_cards)
        hand_cards.append(self.turn_card)
        hand_cards.append(self.river_card)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )


@dataclass
class Showdown(State):
    """
    Previous states:
        * PostRiverBetting -> FinishPostRiverBetting

    Next states:
        * PlayerFolds -> Showdown
        * PlayerRevealsHand -> Showdown
        * RankHands -> DistributingPots
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    deck: Deck
    hand_player_hole_cards: list[Tuple[Card, Card]]
    hand_player_has_folded: list[bool]
    pots: list[Pot]
    flop_cards: Tuple[Card, Card, Card]
    turn_card: Card
    river_card: Card
    hand_player_has_revealed_hand: list[bool]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate cards in the hand.
        hand_cards = [
            hole_card
            for hand_player_hole_cards in self.hand_player_hole_cards
            for hole_card in hand_player_hole_cards
        ]
        hand_cards.extend(self.deck)
        hand_cards.extend(self.flop_cards)
        hand_cards.append(self.turn_card)
        hand_cards.append(self.river_card)
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )

        # Validate hole cards of players in the hand.
        validate_state(
            len(self.hand_player_hole_cards) == len(self.hand_player_ids),
            "Every player in the hand must have hole cards.",
        )

        # Validate folded players in the hand.
        validate_state(
            len(self.hand_player_has_folded) == len(self.hand_player_ids),
            "Every player in the hand must have folded or not have folded.",
        )
        validate_state(
            not all(self.hand_player_has_folded),
            "At least 1 player in the hand must not have folded.",
        )

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            not self.hand_player_has_folded[
                                self.hand_player_ids.index(player_id)
                            ]
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least one player in the hand who has not folded.",
        )

        # Validate revealed hands by players in the hand.
        validate_state(
            len(self.hand_player_has_revealed_hand) == len(self.hand_player_ids),
            "Every player in the hand must have revealed their hand or not have "
            "revealed their hand.",
        )
        validate_state(
            not any(
                [
                    hand_player_has_folded and hand_player_has_revealed_hand
                    for hand_player_has_folded, hand_player_has_revealed_hand in zip(
                        self.hand_player_has_folded, self.hand_player_has_revealed_hand
                    )
                ]
            ),
            "A player cannot have folded and have revealed their hand.",
        )


@dataclass
class DistributingPots(State):
    """
    Previous states:
        * Showdown -> RankHands
        * PreFlopBetting -> DeclareDefaultWinner
        * PostFlopBetting -> DeclareDefaultWinner
        * PostTurnBetting -> DeclareDefaultWinner
        * PostRiverBetting -> DeclareDefaultWinner

    Next states:
        * DistributePots -> PostHand
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]
    hand_player_ids: list[PlayerID]
    pots: list[Pot]
    hand_ranking_player_ids: list[PlayerID]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

        # Validate players in the hand.
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

        # Validate pots in the hand.
        validate_state(
            all(
                [
                    all([player_id in self.player_ids for player_id in pot.player_ids])
                    for pot in self.pots
                ]
            ),
            "For every pot in the hand, every player in the pot must be a player in "
            "the game.",
        )
        validate_state(
            all(
                [
                    any(
                        [
                            player_id in self.hand_ranking_player_ids
                            for player_id in pot.player_ids
                        ]
                    )
                    for pot in self.pots
                ]
            ),
            "Every pot must have at least 1 player in the ranking.",
        )

        # Validate ranking of players in the hand.
        validate_state(
            all(
                [
                    player_id in self.hand_player_ids
                    for player_id in self.hand_ranking_player_ids
                ]
            ),
            "Every player in the ranking must be a player in the hand.",
        )


@dataclass
class PostHand:
    """
    Previous States:
        * DistributingPots -> DistributePots

    Next States:
        * StartHand -> SettingBlinds
        * EndGame -> GameOver
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )


@dataclass
class GameEnded:
    """
    Previous States:
        * BuyingIn -> EndGame
        * PostHand -> EndGame
    """

    player_ids: list[PlayerID]
    player_stacks: list[NumChips]

    def __post_init__(self) -> None:
        # Validate players in the game.
        validate_state(
            len(self.player_ids) <= 23,
            "The number of players must be less than or equal to 23.",
        )
        validate_state(
            len(self.player_ids) == len(set(self.player_ids)),
            "Every player must have a unique ID.",
        )

        # Validate stacks of players in the game.
        validate_state(
            len(self.player_stacks) == len(self.player_ids),
            "Every player must have a stack.",
        )
        validate_state(
            all([player_stack >= 0 for player_stack in self.player_stacks]),
            "Every player must have a non-negative stack.",
        )

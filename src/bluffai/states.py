from dataclasses import dataclass

from bluffai.types import Card, Deck, NumChips, PlayerID, Pot, State
from bluffai.validate import validate_state

StateType = str
PlayerPosition = int


@dataclass(frozen=True, kw_only=True)
class StartingGame(State):
    """
    No previous states.

    Next states:
        * StartHand -> SettingBlinds
        * EndGame -> GameOver
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]

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


@dataclass(frozen=True, kw_only=True)
class SettingBlinds(State):
    """
    Previous states:
        * BuyingIn -> StartHand

    Next states:
        * SetBlinds -> PlacingBlinds
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]

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


@dataclass(frozen=True, kw_only=True)
class PlacingBlinds(State):
    """
    Previous states:
        * SettingBlinds -> SetBlinds

    Next states:
        * PlaceBlinds -> ShufflingDeck
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
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


@dataclass(frozen=True, kw_only=True)
class ShuffleDeck(State):
    """
    Previous states:
        * PlacingBlinds -> PlaceBlinds

    Next states:
        * ShuffleDeck -> DealingHoleCards
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: tuple[NumChips, ...]

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


@dataclass(frozen=True, kw_only=True)
class DealingHoleCards(State):
    """
    Previous states:
        * ShufflingDeck -> ShuffleDeck

    Next states:
        * DealHoleCards -> PreFlopBetting
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: tuple[NumChips, ...]
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
        hand_cards = self.deck
        validate_state(
            len(hand_cards) == 52,
            "There must be 52 total cards in the hand.",
        )
        validate_state(
            len(hand_cards) == len(set(hand_cards)),
            "Every card in the hand must be unique.",
        )


@dataclass(frozen=True, kw_only=True)
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

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: tuple[NumChips, ...]
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]

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
        hand_cards = self.deck + tuple(
            [
                hole_card
                for hand_player_hole_cards in self.hand_player_hole_cards
                for hole_card in hand_player_hole_cards
            ]
        )
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


@dataclass(frozen=True, kw_only=True)
class DealingFlopCards(State):
    """
    Previous states:
        * PreFlopBetting -> FinishPreFlopBetting

    Next states:
        * DealFlopCards -> PostFlopBetting
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]

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
        hand_cards = self.deck + tuple(
            [
                hole_card
                for hand_player_hole_cards in self.hand_player_hole_cards
                for hole_card in hand_player_hole_cards
            ]
        )
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


@dataclass(frozen=True, kw_only=True)
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

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: tuple[NumChips, ...]
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]
    flop_cards: tuple[Card, Card, Card]

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
        hand_cards = (
            self.deck
            + tuple(
                [
                    hole_card
                    for hand_player_hole_cards in self.hand_player_hole_cards
                    for hole_card in hand_player_hole_cards
                ]
            )
            + self.flop_cards
        )
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


@dataclass(frozen=True, kw_only=True)
class DealingTurnCard(State):
    """
    Previous states:
        * PostFlopBetting -> FinishPostFlopBetting

    Next states:
        * DealTurnCard -> PostTurnBetting
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]
    flop_cards: tuple[Card, Card, Card]

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
        hand_cards = (
            self.deck
            + tuple(
                [
                    hole_card
                    for hand_player_hole_cards in self.hand_player_hole_cards
                    for hole_card in hand_player_hole_cards
                ]
            )
            + self.flop_cards
        )
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


@dataclass(frozen=True, kw_only=True)
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

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: tuple[NumChips, ...]
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]
    flop_cards: tuple[Card, Card, Card]
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
        hand_cards = (
            self.deck
            + tuple(
                [
                    hole_card
                    for hand_player_hole_cards in self.hand_player_hole_cards
                    for hole_card in hand_player_hole_cards
                ]
            )
            + self.flop_cards
            + (self.turn_card,)
        )
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


@dataclass(frozen=True, kw_only=True)
class DealingRiverCard(State):
    """
    Previous states:
        * PostTurnBetting -> FinishPostTurnBetting

    Next states:
        * DealRiverCard -> PostRiverBetting
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]
    flop_cards: tuple[Card, Card, Card]
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
        hand_cards = (
            self.deck
            + tuple(
                [
                    hole_card
                    for hand_player_hole_cards in self.hand_player_hole_cards
                    for hole_card in hand_player_hole_cards
                ]
            )
            + self.flop_cards
            + (self.turn_card,)
        )
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


@dataclass(frozen=True, kw_only=True)
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

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    little_blind: NumChips
    big_blind: NumChips
    hand_player_bets: tuple[NumChips, ...]
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]
    flop_cards: tuple[Card, Card, Card]
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
        hand_cards = (
            self.deck
            + tuple(
                [
                    hole_card
                    for hand_player_hole_cards in self.hand_player_hole_cards
                    for hole_card in hand_player_hole_cards
                ]
            )
            + self.flop_cards
            + (self.turn_card, self.river_card)
        )
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


@dataclass(frozen=True, kw_only=True)
class Showdown(State):
    """
    Previous states:
        * PostRiverBetting -> FinishPostRiverBetting

    Next states:
        * PlayerFolds -> Showdown
        * PlayerRevealsHand -> Showdown
        * RankHands -> DistributingPots
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    deck: Deck
    hand_player_hole_cards: tuple[tuple[Card, Card], ...]
    hand_player_has_folded: tuple[bool, ...]
    pots: tuple[Pot, ...]
    flop_cards: tuple[Card, Card, Card]
    turn_card: Card
    river_card: Card
    hand_player_has_revealed_hand: tuple[bool, ...]

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
        hand_cards = (
            self.deck
            + tuple(
                [
                    hole_card
                    for hand_player_hole_cards in self.hand_player_hole_cards
                    for hole_card in hand_player_hole_cards
                ]
            )
            + self.flop_cards
            + (self.turn_card, self.river_card)
        )
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


@dataclass(frozen=True, kw_only=True)
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

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]
    hand_player_ids: tuple[PlayerID, ...]
    pots: tuple[Pot, ...]
    hand_ranking_player_ids: tuple[PlayerID, ...]

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


@dataclass(frozen=True, kw_only=True)
class PostHand(State):
    """
    Previous States:
        * DistributingPots -> DistributePots

    Next States:
        * StartHand -> SettingBlinds
        * EndGame -> GameOver
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]

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


@dataclass(frozen=True, kw_only=True)
class GameOver(State):
    """
    Previous States:
        * BuyingIn -> EndGame
        * PostHand -> EndGame
    """

    player_ids: tuple[PlayerID, ...]
    player_stacks: tuple[NumChips, ...]

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

import random
import uuid
from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Dict, NewType, Tuple

RoomID = NewType("RoomID", uuid.UUID)
"""
The unique ID of a poker room.
"""

PlayerID = NewType("PlayerID", uuid.UUID)
"""
The unique ID of a poker player in a `Room`.
"""

PlayerAgentAddress = NewType("PlayerAgentAddress", str)
"""
The IP address of a poker player agent.
"""

NumChips = NewType("NumChips", int)
"""
The number of chips.
"""

RandomSeed = int | float | str | bytes | bytearray | None
"""
The seed value for a pseudo-random number generator.
"""


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


class Deck:
    """
    Represents the state of a deck of cards.
    """

    _random: random.Random
    _cards: list[Card]

    def __init__(self, random_seed: RandomSeed = None):
        """
        Args:
            random_seed: The seed value for the pseudo-random number generator that
            shuffles the deck of cards
        """
        self._random = random.Random(random_seed)
        self._cards = [
            Card.CLUBS_2,
            Card.CLUBS_3,
            Card.CLUBS_4,
            Card.CLUBS_5,
            Card.CLUBS_6,
            Card.CLUBS_7,
            Card.CLUBS_8,
            Card.CLUBS_9,
            Card.CLUBS_10,
            Card.CLUBS_JACK,
            Card.CLUBS_QUEEN,
            Card.CLUBS_KING,
            Card.CLUBS_ACE,
            Card.DIAMONDS_2,
            Card.DIAMONDS_3,
            Card.DIAMONDS_4,
            Card.DIAMONDS_5,
            Card.DIAMONDS_6,
            Card.DIAMONDS_7,
            Card.DIAMONDS_8,
            Card.DIAMONDS_9,
            Card.DIAMONDS_10,
            Card.DIAMONDS_JACK,
            Card.DIAMONDS_QUEEN,
            Card.DIAMONDS_KING,
            Card.DIAMONDS_ACE,
            Card.HEARTS_2,
            Card.HEARTS_3,
            Card.HEARTS_4,
            Card.HEARTS_5,
            Card.HEARTS_6,
            Card.HEARTS_7,
            Card.HEARTS_8,
            Card.HEARTS_9,
            Card.HEARTS_10,
            Card.HEARTS_JACK,
            Card.HEARTS_QUEEN,
            Card.HEARTS_KING,
            Card.HEARTS_ACE,
            Card.SPADES_2,
            Card.SPADES_3,
            Card.SPADES_4,
            Card.SPADES_5,
            Card.SPADES_6,
            Card.SPADES_7,
            Card.SPADES_8,
            Card.SPADES_9,
            Card.SPADES_10,
            Card.SPADES_JACK,
            Card.SPADES_QUEEN,
            Card.SPADES_KING,
            Card.SPADES_ACE,
        ]

    def shuffle(self) -> None:
        """
        Shuffles the cards in the deck.
        """
        self._random.shuffle(self._cards)

    def deal_card(self) -> Card:
        """
        Removes the top deal_card from the deck and returns it.
        """
        return self._cards.pop()


class NotEnoughPlayersInHandError(Exception):
    """
    Attempted to play a hand of poker with too few players. A hand must have at least 2
    players.
    """


@dataclass
class Hand:
    """
    `Hand` represents the state of a hand in a game of Texas Hold'em poker.
    """

    _player_ids: list[PlayerID]
    _player_hole_cards: dict[PlayerID, Tuple[Card, Card]]
    _flop_cards: Tuple[Card, Card, Card]
    _turn_card: Card
    _river_card: Card
    _big_blind_num_chips: NumChips
    _little_blind_num_chips: NumChips

    def __init__(
        self,
        player_ids: list[PlayerID],
        big_blind_num_chips: NumChips,
        little_blind_num_chips: NumChips,
    ):
        """
        Args:
            player_ids: A list of player IDs for players participating in the poker
            hand.

        Raises:
            NotEnoughPlayersInHandError
        """
        if len(player_ids) < 2:
            raise NotEnoughPlayersInHandError

        deck = Deck()
        deck.shuffle()

        self._player_hold_cards = {
            player_id: (deck.deal_card(), deck.deal_card())
            for player_id in self._player_ids
        }

        self._flop_cards = (deck.deal_card(), deck.deal_card(), deck.deal_card())
        self._turn_card = deck.deal_card()
        self._river_card = deck.deal_card()

        self._big_blind_num_chips = big_blind_num_chips
        self._little_blind_num_chips = little_blind_num_chips
    
    def play_preflop_round(self):
        


@dataclass
class Game:
    """
    `Game` represents the state of a game of Texas Hold'em poker.
    """

    _player_ids: list[PlayerID]
    _player_num_chips: dict[PlayerID, NumChips]
    _big_blind_num_chips: NumChips
    _little_blind_num_chips: NumChips

    def __init__(
        self,
        player_ids: list[PlayerID],
        buy_in_num_chips: NumChips,
        big_blind_num_chips: NumChips,
        little_blind_num_chips: NumChips,
    ) -> None:
        """
        Args:
            player_ids: A list of player IDs for players in the poker game.

            buy_in_num_chips: The starting number of chips for each player.

            big_blind_num_chips: The number of chips that the big blind player must bet
            at the beginning of each hand.

            little_blind_num_chips: The number of chips that the little blind player
            must bet at the beginning of each hand.
        """
        self._player_ids = player_ids
        self._player_num_chips = {
            player_id: buy_in_num_chips for player_id in self._player_ids
        }
        self._big_blind_num_chips = big_blind_num_chips
        self._little_blind_num_chips = little_blind_num_chips

    def play_hand(self) -> None:
        """
        Simulates a hand of poker with the players in the `Game`.

        Args:
            game: The state of the game before playing the hand of poker.

        Returns:
            The state of the game after playing a hand of poker.

        Raises:
            GameUnplayableError
        """
        hand = Hand(
            player_ids=self.player_ids_with_chips(),
            big_blind_num_chips=self._big_blind_num_chips,
            little_blind_num_chips=self._little_blind_num_chips,
        )

        hand.play_preflop_round()

    def player_ids_with_chips(self) -> list[PlayerID]:
        return list(
            filter(
                lambda player_id: self._player_num_chips[player_id] > 0,
                self._player_ids,
            ),
        )


@dataclass
class Room:
    """
    `Room` represents a room for playing games of poker.
    """

    _id: RoomID
    _player_agent_addresses: Dict[PlayerID, PlayerAgentAddress]
    _random_seed: RandomSeed

    def __init__(self, random_seed=None) -> None:
        self._id = RoomID(uuid.uuid4())
        self._player_agent_addresses = {}
        self._random_seed = random_seed

    def add_player(
        self,
        player_id: PlayerID,
        player_agent_address: PlayerAgentAddress,
    ) -> None:
        """
        Adds a player to the `Room`.

        Args:
            player_id: The unique ID of the player.

            player_agent_address: The IP address of the player agent.
        """
        self._player_agent_addresses[player_id] = player_agent_address

    def play_game(
        self,
        buy_in_num_chips: NumChips,
        little_blind_num_chips: NumChips,
        big_blind_num_chips: NumChips,
    ) -> None:
        """
        Simulates a game of poker with the players in the `Room`.

        Args:
            buy_in_num_chips: The starting number of chips for each player.

            big_blind_num_chips: The number of chips that the big blind player must bet
            at the beginning of each hand.

            little_blind_num_chips: The number of chips that the little blind player
            must bet at the beginning of each hand.
        """
        game_rng = random.Random(self._random_seed)

        # Randomize the order of player actions in the poker game.
        player_ids = list(self._player_agent_addresses.keys())
        game_rng.shuffle(player_ids)

        # Initialize the poker game.
        game = Game(
            player_ids=player_ids,
            buy_in_num_chips=buy_in_num_chips,
            little_blind_num_chips=little_blind_num_chips,
            big_blind_num_chips=big_blind_num_chips,
        )

        while True:
            game.play_hand()

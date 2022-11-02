import importlib
import pathlib
import random
import sys
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto, unique
from typing import Any, NewType, NoReturn, Sized, Tuple

import click

from bluffai.__version__ import __version__


class AgentTestFailure(Exception):
    pass


class _ExitCode(int, Enum):
    OK = 0
    ERROR = 1


def main() -> NoReturn:
    sys.exit(_bluffai_cli(standalone_mode=False))


@click.group(name="bluffai")
@click.help_option("-h", "--help")
@click.version_option(__version__, "-v", "--version")
def _bluffai_cli() -> None:
    pass


@_bluffai_cli.command(
    name="test",
    help="Checks that your bluffai agent is ready for poker simulation.",
)
@click.help_option("-h", "--help")
def _test() -> _ExitCode:
    try:
        agent = _import_agent()
    except ImportError as exc:
        raise AgentTestFailure(
            "Could not find the file `main.py` in your current working directory. To "
            "fix this error, you must store your bluffai agent instance in a variable "
            "`agent` in a file `main.py`."
        ) from exc
    except AttributeError as exc:
        raise AgentTestFailure(
            "Could not find the variable `agent` in the file `main.py`. To fix this "
            "error, you must store your bluffai agent instance in a variable `agent` "
            "in a file `main.py`."
        ) from exc

    if not isinstance(agent, Agent):
        raise AgentTestFailure(
            f"Agent type {type(agent)} is not a subclass of {Agent}. To fix this "
            f"error, you must make {type(agent)} a subclass of {Agent}."
        )

    try:
        state = State()
        agent.observe_state(state)
    except NotImplementedError as exc:
        raise AgentTestFailure(
            "Agent method `observe_state` is not implemented. To fix this error, you "
            "must override the method `observe_state` with your own implementation."
        ) from exc

    try:
        event: Event = {}
        agent.observe_event(event)
    except NotImplementedError as exc:
        raise AgentTestFailure(
            "Agent method `observe_event` is not implemented. To fix this error, you "
            f"must create a subclass of {Agent} and override the method "
            "`observe_event` with your own implementation."
        ) from exc

    try:
        state = State()
        player_id = "player-0"
        action = agent.decide_action(player_id, state)
    except NotImplementedError as exc:
        raise AgentTestFailure(
            "Agent method `decide_action` is not implemented. To fix this error, you "
            f"must create a subclass of {Agent} and override the method "
            "`decide_action` with your own implementation."
        ) from exc

    if not isinstance(action, Action):
        raise AgentTestFailure(
            f"{agent.decide_action} returned the value {action} with type "
            f"{type(action)}, which is not equal to the type {Action}. Your "
            "implementation of the method `decide_action` must return a value with "
            f"type {Action}."
        )

    state = State()
    player_id = PlayerID("player-0")
    action = agent.decide_action(player_id, state)
    try:
        state.apply_action(action)
    except InvalidActionError as exc:
        raise AgentTestFailure(
            f"{agent.decide_action} returned an invalid action. Your implementation of "
            "the method `decide_action` must comply with the rules of the game of "
            "Texas Hold'em poker."
        ) from exc
    except InvalidActionForStateError as exc:
        raise AgentTestFailure(
            f"{agent.decide_action} returned an invalid action for the given game "
            "state. Your implementation of the method `decide_action` must comply with "
            "the rules of the game of Texas Hold'em poker."
        ) from exc

    print("All tests have passed. Your bluffai agent is ready for poker simulation.")
    return _ExitCode.OK


def _import_agent() -> "Agent":
    sys.path.insert(0, str(pathlib.Path.cwd()))
    module = importlib.import_module("main")
    agent = getattr(module, "agent")
    return agent


RoomID = NewType("RoomID", uuid.UUID)
"""
A unique ID of a poker room.
"""

PlayerID = str
"""
A unique ID of a poker player in a `Room`.
"""

PlayerAgentAddress = NewType("PlayerAgentAddress", str)
"""
An IP address of a poker player agent.
"""

NumChips = int
"""
A number of chips.
"""

RandomSeed = int | float | str | bytes | bytearray | None
"""
A seed value for a pseudo-random number generator.
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


class Deck(Sized):
    """
    Represents the state of a deck of cards.
    """

    _random: random.Random
    _cards: list[Card]

    def __init__(self, random_seed: RandomSeed = None) -> None:
        """
        Args:
            random_seed (RandomSeed): The seed value for the pseudo-random number
                generator that shuffles the deck of cards
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

    def __len__(self) -> int:
        return len(self._cards)

    def shuffle(self) -> None:
        """
        Shuffles the cards in the deck.
        """
        self._random.shuffle(self._cards)

    def deal_card(self) -> Card:
        """
        Removes the top card from the deck and returns it.

        Returns:
            Card: the top card in the deck.
        """
        return self._cards.pop()


class ActionType(Enum):
    """
    `ActionType` enumerates the type of actions that an agent can take during a game of
    Texas Hold'em poker.
    """

    CALL = "call"
    CHECK = "check"
    FOLD = "fold"
    RAISE = "raise"


class EventType(Enum):
    PLAYER_FOLDED = "player_folded"
    PLAYER_CHECKED = "player_checked"
    PLAYER_CALLED = "player_called"
    PLAYER_RAISED = "player_raised"


Event = dict[str, Any]


@dataclass
class Action:
    """
    `Action` represents an action that an `Agent` can take during a game of Texas
    Hold'em poker.
    """

    player_id: PlayerID
    type: ActionType
    bet: NumChips | None = None

    def validate(self) -> None:
        if self.type == ActionType.CALL:
            if self.bet is None or self.bet == 0:
                raise InvalidActionError(
                    f"Action with type {ActionType.CALL} has bet {self.bet}. Actions "
                    f"with type {ActionType.CALL} must have a positive bet value."
                )

        if self.type == ActionType.RAISE:
            if self.bet is None or self.bet == 0:
                raise InvalidActionError(
                    f"Action with type {ActionType.RAISE} has bet {self.bet}. Actions "
                    f"with type {ActionType.RAISE} must have a positive bet value."
                )

    def to_event(self) -> Event:
        if self.type == ActionType.FOLD:
            return {
                "type": EventType.PLAYER_FOLDED,
                "player_id": self.player_id,
            }

        if self.type == ActionType.CHECK:
            return {
                "type": EventType.PLAYER_CHECKED,
                "player_id": self.player_id,
            }

        if self.type == ActionType.CALL:
            return {
                "type": EventType.PLAYER_CALLED,
                "player_id": self.player_id,
                "num_chips": self.bet,
            }

        if self.type == ActionType.RAISE:
            return {
                "type": EventType.PLAYER_RAISED,
                "player_id": self.player_id,
                "num_chips": self.bet,
            }

        raise RuntimeError


class InvalidActionForStateError(Exception):
    """
    `InvalidActionForStateError` is raised when an `Action` cannot be applied to a
    given `State`.
    """


class InvalidActionError(Exception):
    """
    `InvalidActionError` is raised when an `Action` is invalid.
    """


@dataclass
class Player:
    """
    `Player` represents the state of a player ina game of Texas Hold'em poker.
    """

    id: PlayerID
    stack: NumChips
    bet: NumChips = 0
    has_folded: bool = False


@dataclass
class State:
    """
    `State` represents the state of a game of Texas Hold'em poker.
    """

    players: list[Player] = field(default_factory=list)
    player_bets: dict[PlayerID, NumChips] = field(default_factory=dict)
    player_stacks: dict[PlayerID, NumChips] = field(default_factory=dict)
    player_has_folded: dict[PlayerID, bool] = field(default_factory=dict)
    player_ids: list[PlayerID] = field(default_factory=list)

    @property
    def largest_bet(self) -> NumChips:
        """
        Returns the largest bet for the current betting round.

        Returns:
            NumChips: the number of chips in the largest bet
        """
        if self.players == []:
            return 0
        return max([player.bet for player in self.players])

    def player(self, player_id: PlayerID) -> Player | None:
        """
        Returns the player in the game with ID `player_id`, or returns `None` if there
        is no player in the game with ID `player_id`.

        Args:
            player_id (PlayerID): the ID of the player

        Returns:
            Player | None: the player in the game, or `None` if the player is not in the
                game
        """
        for player in self.players:
            if player.id == player_id:
                return player
        return None


def apply(state: State, action: Action) -> None:
    """
    Applies the `action` to the `state`, simulating an action being performed in the
    game of Texas Hold'em poker.

    Args:
        state ()
        action (Action): the action to apply to the game.
    """
    if action.type == ActionType.FOLD:
        player = state.player(action.player_id)
        assert player is not None
        player.has_folded = True
        return

    if action.type == ActionType.CHECK:
        return

    if action.type == ActionType.CALL or action.type == ActionType.RAISE:
        assert action.bet is not None
        player = state.player(action.player_id)
        assert player is not None
        player.bet = action.bet
        return


def validate_action_for_state(state: State, action: Action) -> None:
    """
    Validates that the `action` can be applied to the `state`, according to the rules
    of Texas Hold'em poker.

    Args:
        state (State): the state of the game of Texas Hold'em poker.
        action (Action): the action to be applied to the `state`.
    """
    if action.player_id not in state.player_ids:
        raise InvalidActionForStateError(
            "Cannot apply an action for a player that is not in the game."
        )

    if action.type == ActionType.CHECK:
        if state.largest_bet != 0:
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.CHECK} when there "
                "is an existing bet in the current betting round."
            )

    if action.type == ActionType.CALL:
        if state.largest_bet == 0:
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.CALL} when there "
                "is no existing bet in the current betting round."
            )

        assert action.bet is not None
        if action.bet > state.player_stacks[action.player_id]:
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.CALL} and a bet "
                "that is greater than the player's stack of chips."
            )
        if action.bet > state.largest_bet:
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.CALL} and a bet "
                "that is greater than the largest bet in the current betting round."
            )
        if (
            action.bet < state.largest_bet
            and action.bet != state.player_stacks[action.player_id]
        ):
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.CALL} and a bet "
                "that is less than the largest bet in the current betting "
                "round without going all-in."
            )

    if action.type == ActionType.RAISE:
        assert action.bet is not None
        if action.bet > state.player_stacks[action.player_id]:
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.RAISE} and a bet "
                "that is greater than the player's stack of chips."
            )
        if action.bet <= state.largest_bet:
            raise InvalidActionForStateError(
                f"Cannot apply an action with type {ActionType.RAISE} and a bet "
                "that is less than or equal to the largest bet in the current "
                "betting round."
            )


def apply_action(state: State, action: Action) -> None:
    """
    Updates the current state based on the `action`.

    Args:
        action (Action): the action to apply to the game.
    """
    if action.type == ActionType.FOLD:
        player = state.player(action.player_id)
        assert player is not None
        player.has_folded = True
        return

    if action.type == ActionType.CHECK:
        return

    if action.type == ActionType.CALL or action.type == ActionType.RAISE:
        assert action.bet is not None
        player = state.player(action.player_id)
        assert player is not None
        player.bet = action.bet
        return


class Agent:
    """
    `Agent` is a base class for implementing agents in a game of Texas Hold'em poker.

    This class is not intended to be instantiated directly. Instead, you should create
    your own subclass of `Agent` and override the following methods:

    - `observe_state(self, state: State) -> None`
    - `observe_event(self, event: Event) -> None`
    - `decide_action(self, game_state: State) -> Action`
    """

    def observe_state(self, state: State) -> None:
        """
        Observes the `state` of the game of Texas Hold'em poker.

        Your agent can use the information in the `state` to decide future actions.

        Args:
            state (State): the state of the game that is being observed.
        """
        raise NotImplementedError

    def observe_event(self, event: Event) -> None:
        """
        Observes the `event` that occurred in the game of Texas Hold'em poker.

        Your agent can use the information in the `event` to decide future actions.

        Args:
            event (Event): the event in the game that is being observed.
        """
        raise NotImplementedError

    def decide_action(self, player_id: PlayerID, state: State) -> Action:
        """
        Returns an action for the player with ID `player_id` in a game of Texas Hold'em
        poker with the given `state`.

        Args:
            player_id (PlayerID): the ID of the player that the action is for.
            state (State): the state of the game that the action will be applied to.

        Returns:
            Action: the action that will be applied to the game.
        """
        raise NotImplementedError


@dataclass
class _Player:
    """
    `Player` represents the state of a player in a `Game`.
    """

    id: PlayerID
    stack_size: NumChips
    hole_cards: Tuple[Card, Card] | None = None
    bet_size: NumChips | None = None
    is_all_in: bool = False
    has_folded: bool = False


Pot = NewType("Pot", dict[PlayerID, NumChips])


@unique
class Round(Enum):
    """
    `Round` is the betting round in a `Game`.
    """

    PREFLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()


class Step:
    """
    `Step` represents a step in a `Game`.
    """


@dataclass(frozen=True)
class StartNewHand(Step):
    """
    `StartNewHand` is a step in a `Game` that starts a new hand.
    """


@dataclass(frozen=True)
class PostLittleBlind(Step):
    """
    `PostLittleBlind` is a step in a `Game` where the player in the little blind
    position must bet the little blind amount.
    """

    player_id: PlayerID


@dataclass(frozen=True)
class PostBigBlind(Step):
    """
    `PostBigBlind` is a step in a `Game` where the player in the big blind position
    must bet the big blind amount.
    """

    player_id: PlayerID


@dataclass(frozen=True)
class PlayerAction(Step):
    """
    `PlayerAction` is a step in a `Game` where a player must decide to check, call,
    raise, or fold.
    """

    player_id: PlayerID


@dataclass
class _Game:
    """
    `Game` represents the state of a game of Texas Hold'em poker.
    """

    big_blind: NumChips
    little_blind: NumChips
    players: list[_Player]
    button_position: int = 0
    round: Round | None = None
    last_raise_player_id: PlayerID | None = None
    last_raise_num_chips: NumChips | None = None
    pots: list[Pot] | None = None
    flop_cards: Tuple[Card, Card, Card] | None = None
    turn_card: Card | None = None
    river_card: Card | None = None

    def next_step(self) -> Step | None:
        if len(self.players) < 2:
            return None

        if self.round is None:
            return StartNewHand()

        if self.round == Round.PREFLOP:
            little_blind_position = (self.button_position + 1) % len(self.players)
            little_blind_player = self.players[little_blind_position]
            if little_blind_player.bet_size is None:
                return PostLittleBlind(little_blind_player.id)

            big_blind_position = (little_blind_position + 1) % len(self.players)
            big_blind_player = self.players[big_blind_position]
            if big_blind_player.bet_size is None:
                return PostBigBlind(big_blind_player.id)


@dataclass
class Room:
    """
    `Room` represents a room for playing games of poker.
    """

    id: RoomID
    players: list[_Player]

    def __init__(self) -> None:
        self.id = RoomID(uuid.uuid4())

    def add_player(self, player: _Player) -> None:
        """
        Adds a player to the `Room`.
        """
        self.players.append(player)


# State(empty) -> Action(create) -> State(s)
# State(s) -> Action(a) -> State(s')


class _StateType(Enum):
    INITIAL = auto()
    SETTING_BIG_BLIND = auto()
    SETTING_LITTLE_BLIND = auto()
    PLAYERS_BUYING_IN = auto()
    STARTING_HAND = auto()
    POSTING_BIG_BLIND = auto()
    POSTING_LITTLE_BLIND = auto()
    DEALING_HOLD_CARDS = auto()
    PRE_FLOP_BETTING = auto()
    DEALING_FLOP_CARDS = auto()
    POST_FLOP_BETTING = auto()
    DEALING_TURN_CARD = auto()
    POST_TURN_BETTING = auto()
    DEALING_RIVER_CARD = auto()
    POST_RIVER_BETTING = auto()
    SHOWDOWN = auto()
    ENDING_HAND = auto()
    TERMINAL = auto()


# 1. Validate state.
@dataclass
class _State:
    type: _StateType
    big_blind: NumChips | None = None
    little_blind: NumChips | None = None

    def __post_init__(self) -> None:
        match self.type:
            case _StateType.INITIAL | _StateType.SETTING_BIG_BLIND:
                assert self.big_blind is None
                assert self.little_blind is None
            case _StateType.SETTING_LITTLE_BLIND:
                assert self.big_blind is not None
                assert self.little_blind is None

    @property
    def is_terminal(self) -> bool:
        return False


# 2. Determine next action.
def next_action(state: _State) -> _Action:
    if state.big_blind is None:
        return _Action(
            type=ActionType.SETS_BIG_BLIND,
            big_blind=2,
        )


# 3. Validate action.
@dataclass
class _Action:
    def __post_init__(self) -> None:
        pass


# 4. Validate action for state.
@dataclass
class _Event:
    state: _State
    action: _Action

    def __post_init__(self) -> None:
        pass


# 5. Determine next state.
def next_state(event: _Event) -> _State:
    raise NotImplemented


# 6. Log action as event.
def play_game():
    events = []
    state = _State()
    while True:
        action = next_action(state)
        event = _Event(state, action)
        state = next_state(event)
        events.append(event)
        if state.is_terminal:
            break


# Actions
# -------
# PlayerFolds
# PlayerChecks
# PlayerCalls
# PlayerRaises
# StartsGame(big_blind, little_blind)
# EndsGame
# AddsPlayer
# StartsHand
# DealsHoleCards
# RevealsFlopCards
# RevealsTurnCards
# RevealsRiverCards
# SkipsPlayer
# StartsShowdown
# PlayerReveals

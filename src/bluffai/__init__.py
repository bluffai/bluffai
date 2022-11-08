import importlib
import pathlib
import sys
from dataclasses import dataclass
from enum import Enum
from typing import NoReturn

import click

from bluffai import actions, states
from bluffai.__version__ import __version__
from bluffai.agent import Agent
from bluffai.types import Action, NumChips, PlayerID, State


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

    print("All tests have passed. Your bluffai agent is ready for poker simulation.")
    return _ExitCode.OK


def _import_agent() -> Agent:
    sys.path.insert(0, str(pathlib.Path.cwd()))
    module = importlib.import_module("main")
    agent = getattr(module, "agent")
    return agent


@dataclass
class Event:
    previous_state: State
    action: Action
    next_state: State


class UnexpectedStateError(Exception):
    pass


class UnexpectedActionForStateError(Exception):
    pass


def _apply(state: State, action: Action) -> Event:
    next_state: State
    match state:
        case states.StartingGame():
            match type(action):
                case actions.StartHand:
                    next_state = states.SettingBlinds(
                        player_ids=state.player_ids,
                        player_stacks=state.player_stacks,
                        hand_player_ids=state.player_ids,
                    )
                    return Event(state, action, next_state)
                case actions.EndGame:
                    next_state = states.GameOver(
                        player_ids=state.player_ids,
                        player_stacks=state.player_stacks,
                    )
                    return Event(state, action, next_state)
                case _:
                    raise UnexpectedActionForStateError
        case states.SettingBlinds():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.PlacingBlinds():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.ShuffleDeck():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.DealingHoleCards():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.PreFlopBetting():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.DealingFlopCards():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.PostFlopBetting():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.DealingTurnCard():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.PostTurnBetting():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.DealingRiverCard():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.PostRiverBetting():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.Showdown():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.DistributingPots():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.PostHand():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case states.GameOver():
            match type(action):
                case _:
                    raise UnexpectedActionForStateError
        case _:
            raise UnexpectedStateError


def _fetch_buy_in() -> NumChips:
    return 100


def _fetch_player_ids() -> tuple[PlayerID, ...]:
    return ("player-0", "player-1")


def _decide_action(state: State) -> Action:
    match state:
        case states.StartingGame():
            hand_player_ids = tuple(
                [
                    player_id
                    for player_id, player_stack in zip(
                        state.player_ids, state.player_stacks
                    )
                    if player_stack > 0
                ]
            )
            if len(hand_player_ids) >= 2:
                return actions.StartHand(hand_player_ids=hand_player_ids)
            return actions.EndGame()
        case _:
            raise UnexpectedStateError


def _play_game():
    buy_in = _fetch_buy_in()
    player_ids = _fetch_player_ids()

    state = states.StartingGame(
        player_ids=player_ids,
        player_stacks=(buy_in,) * len(player_ids),
    )
    while type(state) != states.GameOver:
        action = _decide_action(state)
        event = _apply(state, action)
        state = event.next_state

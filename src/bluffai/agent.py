from bluffai.types import Action, Event, PlayerID, State


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

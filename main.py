import bluffai


class MyAgent(bluffai.Agent):
    def observe_event(self, event: bluffai.Event) -> None:
        pass

    def observe_state(self, state: bluffai.State) -> None:
        pass

    def decide_action(
        self,
        player_id: bluffai.PlayerID,
        state: bluffai.State,
    ) -> bluffai.Action:
        return bluffai.Action(player_id=player_id, type=bluffai.ActionType.FOLD)


agent = MyAgent()

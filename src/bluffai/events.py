from dataclasses import dataclass, field

from bluffai import actions, states
from bluffai.types import Event


@dataclass
class PlayerBuysInWhenBuyingIn(Event):
    action: actions.PlayerBuysIn
    previous_state: states.BuyingIn
    next_state: states.BuyingIn = field(init=False)

    def __post_init__(self):
        pass

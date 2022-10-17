from bluffai import NumChips, PlayerAgentAddress, Room


def test_room():
    room = Room()
    addrs = [
        "localhost:8000",
        "localhost:8001",
    ]
    for addr in addrs:
        player_agent_addr = PlayerAgentAddress(addr)
        room.add_player_agent_addr(player_agent_addr)
    room.play_game(
        buy_in_num_chips=NumChips(100),
        little_blind_num_chips=NumChips(1),
        big_blind_num_chips=NumChips(2),
    )

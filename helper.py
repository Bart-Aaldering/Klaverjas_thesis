suits_list = ["Hearth", "Diamond", "Spade", "Club"]
values_list = ["7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

def id_to_suit(id: int) -> str:
    return suits_list[id // 10]

def id_to_value(id: int) -> str:
    return values_list[id % 10]

def strings_to_id(value: str, suit: str) -> int:
    return suits_list.index(suit) * 10 + values_list.index(value)

def values_to_id(value: str) -> int:
    return values_list.index(value)

def suits_to_id(suit: str) -> int:
    return suits_list.index(suit) * 10

def team(player):
    return player % 2

def other_team(player):
    return (player + 1) % 2